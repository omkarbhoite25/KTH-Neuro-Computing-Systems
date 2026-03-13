// motor_common.h -- Shared definitions for all motor control nodes
// Project: Robotic Head
// Author: Omkar Bhoite
// Advised by: Prof. Jorg Conradt & Juan Pablo Romero Bermudez

#ifndef MOTOR_COMMON_H
#define MOTOR_COMMON_H

#include <ros/ros.h>
#include <string>
#include <vector>
#include <cmath>
#include <csignal>
#include "std_msgs/String.h"
#include "multi_motor/GetPosition.h"
#include "multi_motor/Control.h"
#include <dynamixel_sdk/dynamixel_sdk.h>

using namespace dynamixel;

// Control table addresses (MX-28)
constexpr uint16_t ADDR_TORQUE_ENABLE    = 24;
constexpr uint16_t ADDR_GOAL_POSITION    = 30;
constexpr uint16_t ADDR_PRESENT_POSITION = 36;
constexpr uint16_t ADDR_LED              = 25;
constexpr uint16_t ADDR_MOVING_SPEED     = 32;
constexpr uint16_t ADDR_TORQUE           = 34;

// MX-28 position resolution: 4096 ticks for full 360 degrees
constexpr uint16_t MX28_POSITION_RESOLUTION = 4096;
// MX-28 max speed/torque register value
constexpr uint16_t MX28_MAX_SPEED_REG = 1023;
constexpr uint16_t MX28_MAX_TORQUE_REG = 1023;

// Protocol and hardware
constexpr float    PROTOCOL_VERSION = 1.0;
constexpr int      BAUDRATE         = 1000000;
constexpr char     DEVICE_NAME[]    = "/dev/ttyACM0";
constexpr uint16_t DEFAULT_INIT_SPEED = 50;

// Motor configuration struct -- single source of truth per motor
struct MotorConfig {
  uint8_t     id;
  uint16_t    min_pos;
  uint16_t    max_pos;
  uint16_t    default_pos;
  std::string topic_name;
  std::string description;
};

// All 6 motors in the robotic head
static const std::vector<MotorConfig> MOTOR_CONFIGS = {
  {1, 1500, 2500, 2000, "/head_lr",  "Head left-right"},
  {2, 2000, 2900, 2450, "/head_ud",  "Head up-down"},
  {3, 1500, 2500, 2000, "/reye_lr",  "Right eye left-right"},
  {4, 1500, 2500, 2000, "/leye_lr",  "Left eye left-right"},
  {5, 1700, 2300, 2000, "/reye_ud",  "Right eye up-down"},
  {6, 1700, 2300, 2000, "/leye_ud",  "Left eye up-down"},
};

// Global hardware handles
static PortHandler   *portHandler   = nullptr;
static PacketHandler *packetHandler = nullptr;

// Async-signal-safe shutdown flag
static volatile sig_atomic_t g_shutdown_requested = 0;

// Send a 2-byte command to a motor, with error checking
inline bool communicateWithMotor(int id, int addr, int value)
{
  if (packetHandler == nullptr || portHandler == nullptr) {
    ROS_ERROR("Hardware not initialized (null handler)");
    return false;
  }
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

// Validate motor ID is within range (1-6)
inline bool isValidMotorId(int id)
{
  return id >= 1 && id <= 6;
}

// Enable torque on all motors -- returns number of failures
inline int enableTorqueAll()
{
  int failures = 0;
  for (const auto &mc : MOTOR_CONFIGS) {
    if (!communicateWithMotor(mc.id, ADDR_TORQUE_ENABLE, 1))
      failures++;
  }
  if (failures > 0)
    ROS_WARN("Torque enabled on %d/%d motors (%d failed)",
             (int)MOTOR_CONFIGS.size() - failures, (int)MOTOR_CONFIGS.size(), failures);
  else
    ROS_INFO("Torque enabled on all %d motors", (int)MOTOR_CONFIGS.size());
  return failures;
}

// Disable torque on all motors (safe shutdown)
inline void disableTorqueAll()
{
  int failures = 0;
  for (const auto &mc : MOTOR_CONFIGS) {
    if (!communicateWithMotor(mc.id, ADDR_TORQUE_ENABLE, 0))
      failures++;
  }
  if (failures > 0)
    ROS_WARN("Torque disabled on %d/%d motors (%d failed)",
             (int)MOTOR_CONFIGS.size() - failures, (int)MOTOR_CONFIGS.size(), failures);
  else
    ROS_INFO("Torque disabled on all motors");
}

// Set all motors to their default positions at safe speed
inline void setDefaultPositions()
{
  for (const auto &mc : MOTOR_CONFIGS) {
    communicateWithMotor(mc.id, ADDR_MOVING_SPEED, DEFAULT_INIT_SPEED);
  }
  for (const auto &mc : MOTOR_CONFIGS) {
    communicateWithMotor(mc.id, ADDR_GOAL_POSITION, mc.default_pos);
  }
  ROS_INFO("All motors set to default positions");
}

// Initialize hardware: open port, set baudrate. Returns false on failure.
inline bool initHardware()
{
  portHandler = dynamixel::PortHandler::getPortHandler(DEVICE_NAME);
  packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

  if (!portHandler->openPort()) {
    ROS_FATAL("Failed to open port %s!", DEVICE_NAME);
    return false;
  }
  if (!portHandler->setBaudRate(BAUDRATE)) {
    ROS_FATAL("Failed to set baudrate %d! Closing port.", BAUDRATE);
    portHandler->closePort();
    return false;
  }
  ROS_INFO("Hardware initialized: port=%s baudrate=%d", DEVICE_NAME, BAUDRATE);
  return true;
}

// LED blink function
inline void turnLEDonOff(const multi_motor::Control::ConstPtr &msg)
{
  if (!isValidMotorId(msg->id)) {
    ROS_WARN("Invalid motor ID %d for LED", msg->id);
    return;
  }
  for (int blink = 0; blink < 6; blink++) {
    communicateWithMotor((uint8_t)msg->id, ADDR_LED, 1);
    ROS_INFO("LED On");
    sleep(1);
    communicateWithMotor((uint8_t)msg->id, ADDR_LED, 0);
    ROS_INFO("LED Off");
    sleep(1);
  }
}

// Set motor speed (with register range clamping)
inline void movingSpeed(const multi_motor::Control::ConstPtr &msg)
{
  if (!isValidMotorId(msg->id)) {
    ROS_WARN("Invalid motor ID %d for speed", msg->id);
    return;
  }
  uint16_t sp = msg->speed;
  if (sp > MX28_MAX_SPEED_REG) {
    ROS_WARN("Speed %d exceeds max register value %d, clamping", sp, MX28_MAX_SPEED_REG);
    sp = MX28_MAX_SPEED_REG;
  }
  communicateWithMotor((uint8_t)msg->id, ADDR_MOVING_SPEED, sp);
  ROS_INFO("Speed set for motor %d: %d", (uint8_t)msg->id, sp);
}

// Set motor torque (with register range clamping)
inline void setTorque(const multi_motor::Control::ConstPtr &msg)
{
  if (!isValidMotorId(msg->id)) {
    ROS_WARN("Invalid motor ID %d for torque", msg->id);
    return;
  }
  uint16_t tor = msg->torque;
  if (tor > MX28_MAX_TORQUE_REG) {
    ROS_WARN("Torque %d exceeds max register value %d, clamping", tor, MX28_MAX_TORQUE_REG);
    tor = MX28_MAX_TORQUE_REG;
  }
  communicateWithMotor((uint8_t)msg->id, ADDR_TORQUE, tor);
  ROS_INFO("Torque set for motor %d: %d", (uint8_t)msg->id, tor);
}

// Signal handler -- only sets flag (async-signal-safe)
inline void shutdownHandler(int sig)
{
  g_shutdown_requested = 1;
}

// Call from main loop or ros::on_shutdown to perform actual cleanup
inline void performShutdown()
{
  ROS_WARN("Shutting down, disabling torque...");
  disableTorqueAll();
  if (portHandler != nullptr) {
    portHandler->closePort();
  }
}

#endif // MOTOR_COMMON_H
