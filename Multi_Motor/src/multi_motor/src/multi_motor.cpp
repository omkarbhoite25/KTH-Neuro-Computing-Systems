/*******************************************************************************
 * Open terminal #1
 * $ roscore
 * 
 * Open terminal #2
 * $ rosrun multi_motor read_write_node
 * 
 * Open terminal #3 (run one of below commands at a time)
 * $ rostopic pub -1 /set_position multi_motor/Control "{id: 1, position: 0}"
 * $ rostopic pub -1 /set_position multi_motor/Control "{id: 1, position: 1000}"
 * $ rosservice call /get_position "id: 1"

*******************************************************************************/

#include <ros/ros.h>

#include "std_msgs/String.h"
#include "multi_motor/GetPosition.h"
#include "multi_motor/Control.h"
// #include "multi_motor/SetLed.h"
#include "dynamixel_sdk/dynamixel_sdk.h"

using namespace dynamixel;

// Control table address
#define ADDR_TORQUE_ENABLE    24
#define ADDR_GOAL_POSITION    30
#define ADDR_PRESENT_POSITION 36
#define ADDR_LED              25
#define ADDR_MOVING_SPEED     32
#define ADDR_TOQUE            34  

// Protocol version
#define PROTOCOL_VERSION      1.0             // Default Protocol version of DYNAMIXEL X series.

// Default setting
#define DXL1_ID               1               // DXL1 ID
#define DXL2_ID               2               // DXL2 ID
#define DXL3_ID               3               // DXL3 ID
#define DXL4_ID               4               // DXL4 ID
#define DXL5_ID               5               // DXL5 ID
#define DXL6_ID               6               // DXL6 ID
#define BAUDRATE              1000000           // Default Baudrate of DYNAMIXEL X series
#define DEVICE_NAME           "/dev/ttyACM0"  // [Linux] To find assigned port, use "$ ls /dev/ttyUSB*" command

PortHandler *portHandler;
PacketHandler *packetHandler;

bool getPresentPosition(multi_motor::GetPosition::Request &req,
                        multi_motor::GetPosition::Response &res)
{
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;
  
  uint16_t pos = 0;

  dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, (uint8_t)req.id, ADDR_PRESENT_POSITION, &pos, &dxl_error);
  ROS_INFO("getPosition : [ID:%d] -> [POSITION:%d]", req.id, pos);

  res.position = pos;
  return true;
}

void setPositionCallback1(const multi_motor::Control::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", DXL1_ID, msg->position);
}

void setPositionCallback2(const multi_motor::Control::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", DXL2_ID ,msg->position);
}

void setPositionCallback3(const multi_motor::Control::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, DXL3_ID, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", DXL3_ID, msg->position);
}

void setPositionCallback4(const multi_motor::Control::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", DXL4_ID, msg->position);
}

void setPositionCallback5(const multi_motor::Control::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, DXL5_ID, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", DXL5_ID, msg->position);
}

void setPositionCallback6(const multi_motor::Control::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, DXL6_ID, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", DXL6_ID, msg->position);
}







void turnLEDonOff (const multi_motor::Control::ConstPtr &msg)
{
  for (int i=0; i<=10; i++)
  {
    
    uint8_t dxl_error = 0;

    packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_LED, 1, &dxl_error);
    ROS_INFO("LED On");
    sleep(1);
    packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_LED, 0, &dxl_error);
    ROS_INFO("LED Off");
    sleep(1);
  }
}

void movingSpeed (const multi_motor::Control::ConstPtr &msg)
{
  ROS_INFO("Setting new speed");
  uint8_t dxl_error = 0;
  uint16_t sp = (unsigned int)msg->speed;
  packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_MOVING_SPEED, sp, &dxl_error);
  ROS_INFO("New speed set");
}

void setTorque (const multi_motor::Control::ConstPtr &msg)
{
  ROS_INFO("Setting new torque");
  uint8_t dxl_error = 0;
  uint16_t tor = (unsigned int)msg->torque;
  packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_TOQUE, tor, &dxl_error);
  ROS_INFO("New torque set");
}


int main(int argc, char **argv)
{
  uint8_t dxl_error = 0;
  ros::init(argc, argv, "read_write_node");
  ros::NodeHandle nh;

  portHandler = dynamixel::PortHandler::getPortHandler(DEVICE_NAME);
  packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

  if(portHandler->openPort() == false)
  {
    ROS_ERROR("Failed to open the port!");
  }

  if(portHandler->setBaudRate(BAUDRATE) == false)
  {
    ROS_ERROR("Failed to set the baudrate!");
  }
  packetHandler->write2ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  packetHandler->write2ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  packetHandler->write2ByteTxRx(portHandler, DXL3_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  packetHandler->write2ByteTxRx(portHandler, DXL4_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  packetHandler->write2ByteTxRx(portHandler, DXL5_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  packetHandler->write2ByteTxRx(portHandler, DXL6_ID, ADDR_TORQUE_ENABLE, 1, &dxl_error);
  ros::Subscriber set_position1_sub = nh.subscribe("/set_position1", 10, setPositionCallback1);
  ros::Subscriber set_position2_sub = nh.subscribe("/set_position2", 10, setPositionCallback2);
  ros::Subscriber set_position3_sub = nh.subscribe("/set_position3", 10, setPositionCallback3);
  ros::Subscriber set_position4_sub = nh.subscribe("/set_position4", 10, setPositionCallback4);
  ros::Subscriber set_position5_sub = nh.subscribe("/set_position5", 10, setPositionCallback5);
  ros::Subscriber set_position6_sub = nh.subscribe("/set_position6", 10, setPositionCallback6);
  ros::ServiceServer get_position_srv = nh.advertiseService("/get_position", getPresentPosition);
  ros::Subscriber set_speed_sub = nh.subscribe("/set_speed", 10, movingSpeed);
  ros::Subscriber led_sub = nh.subscribe("/led", 10, turnLEDonOff);
  ros::Subscriber set_torque_sub = nh.subscribe("/set_torque", 10, setTorque);


  while (ros::ok())
  {
    usleep(8 * 1000);

    ros::spin();
  }

  return 0;
}
