/*******************************************************************************
 * Open terminal #1
 * $ roscore
 *
 * Open terminal #2
 * $ rosrun single_motor run_single_motor_using_rostopics
 *
 * Open terminal #3 (run one of below commands at a time)
 * $ rostopic pub -1 /set_position single_motor/Control "{id: 1, position: 0}"
 * $ rosservice call /get_position "id: 1"
 *******************************************************************************/

#include <ros/ros.h>
#include <csignal>
#include <cmath>

#include "std_msgs/String.h"
#include "single_motor/GetPosition.h"
#include "single_motor/Control.h"
#include <dynamixel_sdk/dynamixel_sdk.h>

using namespace dynamixel;

// Control table address
constexpr uint16_t ADDR_TORQUE_ENABLE    = 24;
constexpr uint16_t ADDR_GOAL_POSITION    = 30;
constexpr uint16_t ADDR_PRESENT_POSITION = 36;
constexpr uint16_t ADDR_LED              = 25;
constexpr uint16_t ADDR_MOVING_SPEED     = 32;

// Protocol version
constexpr float PROTOCOL_VERSION = 1.0;

// Default setting
constexpr uint8_t DXL1_ID    = 1;
constexpr int     BAUDRATE   = 1000000;
constexpr char    DEVICE_NAME[] = "/dev/ttyACM0";

// MX-28 register limits
constexpr uint16_t MX28_MAX_SPEED_REG = 1023;

PortHandler *portHandler = nullptr;
PacketHandler *packetHandler = nullptr;

// Async-signal-safe shutdown flag
static volatile sig_atomic_t g_shutdown_requested = 0;

// Helper to check write results
static bool writeMotor(uint8_t id, uint16_t addr, uint16_t value)
{
  uint8_t dxl_error = 0;
  int result = packetHandler->write2ByteTxRx(portHandler, id, addr, value, &dxl_error);
  if (result != COMM_SUCCESS) {
    ROS_ERROR("Motor %d write failed at addr %d: %s", id, addr,
              packetHandler->getTxRxResult(result));
    return false;
  }
  if (dxl_error != 0) {
    ROS_ERROR("Motor %d packet error at addr %d: %s", id, addr,
              packetHandler->getRxPacketError(dxl_error));
    return false;
  }
  return true;
}

bool getPresentPosition(single_motor::GetPosition::Request &req,
                        single_motor::GetPosition::Response &res)
{
  if (req.id != DXL1_ID) {
    ROS_ERROR("Invalid motor ID %d (only ID %d supported)", req.id, DXL1_ID);
    return false;
  }
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;
  uint16_t pos = 0;

  dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, (uint8_t)req.id, ADDR_PRESENT_POSITION, &pos, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("getPresentPosition comm failed: %s", packetHandler->getTxRxResult(dxl_comm_result));
    return false;
  }
  if (dxl_error != 0) {
    ROS_ERROR("getPresentPosition packet error: %s", packetHandler->getRxPacketError(dxl_error));
    return false;
  }
  ROS_INFO("getPosition : [ID:%d] -> [POSITION:%d]", req.id, pos);
  res.position = pos * 0.088;
  return true;
}

void setPositionCallback(const single_motor::Control::ConstPtr &msg)
{
  if (msg->id != DXL1_ID) {
    ROS_WARN("Invalid motor ID %d, ignoring", msg->id);
    return;
  }
  if (msg->position > 4095) {
    ROS_WARN("Position %d out of range (0-4095), ignoring", msg->position);
    return;
  }
  uint16_t pos = static_cast<uint16_t>(round(msg->position / 0.088));
  if (pos > 4095) pos = 4095;

  if (!writeMotor((uint8_t)msg->id, ADDR_GOAL_POSITION, pos)) {
    ROS_ERROR("Failed to set position for motor %d", msg->id);
    return;
  }
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", msg->id, pos);
}

void turnLEDonOff(const single_motor::Control::ConstPtr &msg)
{
  if (msg->id != DXL1_ID) {
    ROS_WARN("Invalid motor ID %d for LED", msg->id);
    return;
  }
  for (int blink = 0; blink < 6; blink++) {
    writeMotor((uint8_t)msg->id, ADDR_LED, 1);
    ROS_INFO("LED On");
    sleep(1);
    writeMotor((uint8_t)msg->id, ADDR_LED, 0);
    ROS_INFO("LED Off");
    sleep(1);
  }
}

void movingSpeed(const single_motor::Control::ConstPtr &msg)
{
  if (msg->id != DXL1_ID) {
    ROS_WARN("Invalid motor ID %d for speed", msg->id);
    return;
  }
  // MX-28: 1 register unit = 0.114 RPM, so register = RPM / 0.114
  uint16_t sp = static_cast<uint16_t>(round(msg->speed / 0.114));
  if (sp > MX28_MAX_SPEED_REG) {
    ROS_WARN("Speed register %d exceeds max %d, clamping", sp, MX28_MAX_SPEED_REG);
    sp = MX28_MAX_SPEED_REG;
  }
  writeMotor((uint8_t)msg->id, ADDR_MOVING_SPEED, sp);
  ROS_INFO("Speed set for motor %d: %d", msg->id, sp);
}

// Signal handler -- only sets flag (async-signal-safe)
void shutdownHandler(int sig)
{
  g_shutdown_requested = 1;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "run_single_motor_using_rostopics");
  ros::NodeHandle nh;

  signal(SIGINT, shutdownHandler);

  portHandler = dynamixel::PortHandler::getPortHandler(DEVICE_NAME);
  packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

  if (!portHandler->openPort()) {
    ROS_FATAL("Failed to open port %s!", DEVICE_NAME);
    return 1;
  }

  if (!portHandler->setBaudRate(BAUDRATE)) {
    ROS_FATAL("Failed to set baudrate %d! Closing port.", BAUDRATE);
    portHandler->closePort();
    return 1;
  }

  if (!writeMotor(DXL1_ID, ADDR_TORQUE_ENABLE, 1)) {
    ROS_ERROR("Failed to enable torque on motor %d", DXL1_ID);
  }

  ros::Subscriber set_position_sub = nh.subscribe("/set_position", 10, setPositionCallback);
  ros::ServiceServer get_position_srv = nh.advertiseService("/get_position", getPresentPosition);
  ros::Subscriber set_speed_sub = nh.subscribe("/set_speed", 10, movingSpeed);
  ros::Subscriber led_sub = nh.subscribe("/led", 10, turnLEDonOff);

  ros::Rate rate(125);
  while (ros::ok() && !g_shutdown_requested) {
    ros::spinOnce();
    rate.sleep();
  }

  ROS_WARN("Shutting down, disabling torque...");
  writeMotor(DXL1_ID, ADDR_TORQUE_ENABLE, 0);
  portHandler->closePort();

  return 0;
}
