// Name: Omkar Bhoite
// Project: Robotics Head
// Advised and Guided by: Prof. Jorg Conradt & Juan Pablo Romero Bermudez
//
// multi_motor_radians.cpp -- Controls 6 MX-28 servos using radian-based input.
// Converts radians to ticks: ticks = round((rad + pi) * 4096 / (2*pi))

/*******************************************************************************
 * Open terminal #1
 * $ roscore
 *
 * Open terminal #2
 * $ rosrun multi_motor multi_motor_radians
 *
 * Open terminal #3 (run one of below commands at a time)
 * $ rostopic pub -1 /head_lr multi_motor/Control "{position: 0.0}"
 * $ rosservice call /get_position "id: 1"
 *******************************************************************************/

#include "motor_common.h"

// Convert radians to ticks (MX-28: 4096 positions over 2*pi)
// Clamps result to valid range [0, 4095] to prevent uint16_t UB
static inline uint16_t radToTicks(double rad)
{
  double ticks_d = round((rad + M_PI) * (4096.0 / (2.0 * M_PI)));
  if (ticks_d < 0.0)    ticks_d = 0.0;
  if (ticks_d > 4095.0) ticks_d = 4095.0;
  return static_cast<uint16_t>(ticks_d);
}

// Convert ticks to radians
static inline double ticksToRad(uint16_t ticks)
{
  return ((ticks * 2.0 * M_PI) / 4096.0) - M_PI;
}

// ROS service: get current position in radians
bool getPresentPosition(multi_motor::GetPosition::Request &req,
                        multi_motor::GetPosition::Response &res)
{
  if (!isValidMotorId(req.id)) {
    ROS_ERROR("getPresentPosition: invalid motor ID %d", req.id);
    return false;
  }
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;
  uint16_t pos = 0;
  dxl_comm_result = packetHandler->read2ByteTxRx(
      portHandler, (uint8_t)req.id, ADDR_PRESENT_POSITION, &pos, &dxl_error);
  if (dxl_comm_result != COMM_SUCCESS) {
    ROS_ERROR("getPresentPosition comm failed: %s",
              packetHandler->getTxRxResult(dxl_comm_result));
    return false;
  }
  if (dxl_error != 0) {
    ROS_ERROR("getPresentPosition packet error: %s",
              packetHandler->getRxPacketError(dxl_error));
    return false;
  }
  ROS_INFO("getPosition : [ID:%d] -> [TICKS:%d]", req.id, pos);
  res.position = ticksToRad(pos);
  return true;
}

// Generic position callback -- converts radians to ticks, clamps, then writes
void setPositionCallback(const multi_motor::Control::ConstPtr &msg,
                         const MotorConfig &mc)
{
  double rad = msg->position;
  uint16_t pos = radToTicks(rad);

  if (pos < mc.min_pos) {
    ROS_INFO("Clamping motor %d: %d ticks (%.3f rad) below min, setting to %d",
             mc.id, pos, rad, mc.min_pos);
    pos = mc.min_pos;
  } else if (pos > mc.max_pos) {
    ROS_INFO("Clamping motor %d: %d ticks (%.3f rad) above max, setting to %d",
             mc.id, pos, rad, mc.max_pos);
    pos = mc.max_pos;
  }

  if (!communicateWithMotor(mc.id, ADDR_GOAL_POSITION, pos)) {
    ROS_ERROR("Motor %d (%s) failed to set position %d ticks",
              mc.id, mc.description.c_str(), pos);
    return;
  }
  ROS_INFO("Motor %d (%s) -> %d ticks (%.3f rad)",
           mc.id, mc.description.c_str(), pos, rad);
}

// Speed callback -- converts RPM to register value (MX-28: 1 unit = 0.114 RPM)
// register_value = RPM / 0.114
void movingSpeedRadians(const multi_motor::Control::ConstPtr &msg)
{
  if (!isValidMotorId(msg->id)) {
    ROS_WARN("Invalid motor ID %d for speed", msg->id);
    return;
  }
  double rpm = msg->speed;
  if (rpm < 0.0) {
    ROS_WARN("Negative speed %.2f RPM, ignoring", rpm);
    return;
  }
  uint16_t sp = static_cast<uint16_t>(round(rpm / 0.114));
  if (sp > MX28_MAX_SPEED_REG) {
    ROS_WARN("Speed register %d exceeds max %d, clamping", sp, MX28_MAX_SPEED_REG);
    sp = MX28_MAX_SPEED_REG;
  }
  communicateWithMotor((uint8_t)msg->id, ADDR_MOVING_SPEED, sp);
  ROS_INFO("Speed set for motor %d: %d (%.2f RPM)", (uint8_t)msg->id, sp, rpm);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "multi_motor_radians_node");
  ros::NodeHandle nh;

  signal(SIGINT, shutdownHandler);

  if (!initHardware()) {
    return 1;
  }

  setDefaultPositions();
  enableTorqueAll();

  // Subscribe to per-motor position topics using parameterized callbacks
  std::vector<ros::Subscriber> subs;
  for (const auto &mc : MOTOR_CONFIGS) {
    subs.push_back(nh.subscribe<multi_motor::Control>(
        mc.topic_name, 10,
        [mc](const multi_motor::Control::ConstPtr &msg) {
          setPositionCallback(msg, mc);
        }));
  }

  ros::ServiceServer get_position_srv =
      nh.advertiseService("/get_position", getPresentPosition);
  ros::Subscriber set_speed_sub =
      nh.subscribe("/set_speed", 10, movingSpeedRadians);
  ros::Subscriber led_sub =
      nh.subscribe("/led", 10, turnLEDonOff);
  ros::Subscriber set_torque_sub =
      nh.subscribe("/set_torque", 10, setTorque);

  ros::Rate rate(125);
  while (ros::ok() && !g_shutdown_requested) {
    ros::spinOnce();
    rate.sleep();
  }

  performShutdown();
  return 0;
}
