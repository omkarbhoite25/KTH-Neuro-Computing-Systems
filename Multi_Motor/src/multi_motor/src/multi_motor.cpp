// Name: Omkar Bhoite
// Project: Robotics Head
// Advised and Guided by: Prof. Jorg Conradt & Juan Pablo Romero Bermudez
//
// multi_motor.cpp -- Controls 6 MX-28 servos using tick-based positions.
// Accepts position commands on per-motor ROS topics with range clamping.

/*******************************************************************************
 * Open terminal #1
 * $ roscore
 *
 * Open terminal #2
 * $ rosrun multi_motor multi_motor
 *
 * Open terminal #3 (run one of below commands at a time)
 * $ rostopic pub -1 /head_lr multi_motor/Control "{position: 2000}"
 * $ rosservice call /get_position "id: 1"
 *******************************************************************************/

#include "motor_common.h"

// ROS service: get current position of a motor (in ticks)
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
  ROS_INFO("getPosition : [ID:%d] -> [POSITION:%d]", req.id, pos);
  res.position = pos;
  return true;
}

// Generic position callback -- validates, clamps to motor limits, then writes
void setPositionCallback(const multi_motor::Control::ConstPtr &msg,
                         const MotorConfig &mc)
{
  // Reject negative or out-of-uint16 range values
  if (msg->position < 0.0 || msg->position > 4095.0) {
    ROS_WARN("Motor %d: invalid position %.1f (must be 0-4095), ignoring",
             mc.id, msg->position);
    return;
  }
  uint16_t pos = static_cast<uint16_t>(round(msg->position));

  if (pos < mc.min_pos) {
    ROS_INFO("Clamping motor %d: %d below min, setting to %d",
             mc.id, pos, mc.min_pos);
    pos = mc.min_pos;
  } else if (pos > mc.max_pos) {
    ROS_INFO("Clamping motor %d: %d above max, setting to %d",
             mc.id, pos, mc.max_pos);
    pos = mc.max_pos;
  }

  if (!communicateWithMotor(mc.id, ADDR_GOAL_POSITION, pos)) {
    ROS_ERROR("Motor %d (%s) failed to set position %d",
              mc.id, mc.description.c_str(), pos);
    return;
  }
  ROS_INFO("Motor %d (%s) -> position %d", mc.id, mc.description.c_str(), pos);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "multi_motor_node");
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

  // Shared service and utility subscribers
  ros::ServiceServer get_position_srv =
      nh.advertiseService("/get_position", getPresentPosition);
  ros::Subscriber set_speed_sub =
      nh.subscribe("/set_speed", 10, movingSpeed);
  ros::Subscriber led_sub =
      nh.subscribe("/led", 10, turnLEDonOff);
  ros::Subscriber set_torque_sub =
      nh.subscribe("/set_torque", 10, setTorque);

  // Use spinOnce loop so we can check the async shutdown flag
  ros::Rate rate(125);  // 8ms cycle, same as original
  while (ros::ok() && !g_shutdown_requested) {
    ros::spinOnce();
    rate.sleep();
  }

  performShutdown();
  return 0;
}
