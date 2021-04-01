/*******************************************************************************
 * Open terminal #1
 * $ roscore
 * 
 * Open terminal #2
 * $ rosrun dynamixel_sdk_examples read_write_node
 * 
 * Open terminal #3 (run one of below commands at a time)
 * $ rostopic pub -1 /set_position dynamixel_sdk_examples/SetPosition "{id: 1, position: 0}"
 * $ rostopic pub -1 /set_position dynamixel_sdk_examples/SetPosition "{id: 1, position: 1000}"
 * $ rosservice call /get_position "id: 1"

*******************************************************************************/

#include <ros/ros.h>

#include "std_msgs/String.h"
#include "dynamixel_sdk_examples/GetPosition.h"
#include "dynamixel_sdk_examples/SetPosition.h"
// #include "dynamixel_sdk_examples/SetLed.h"
#include "dynamixel_sdk/dynamixel_sdk.h"

using namespace dynamixel;

// Control table address
#define ADDR_TORQUE_ENABLE    24
#define ADDR_GOAL_POSITION    30
#define ADDR_PRESENT_POSITION 36
#define ADDR_LED              25
#define ADDR_MOVING_SPEED     32

// Protocol version
#define PROTOCOL_VERSION      1.0             // Default Protocol version of DYNAMIXEL X series.

// Default setting
#define DXL1_ID               1               // DXL1 ID
#define BAUDRATE              1000000           // Default Baudrate of DYNAMIXEL X series
#define DEVICE_NAME           "/dev/ttyACM0"  // [Linux] To find assigned port, use "$ ls /dev/ttyUSB*" command

PortHandler *portHandler;
PacketHandler *packetHandler;

bool getPresentPosition(dynamixel_sdk_examples::GetPosition::Request &req,
                        dynamixel_sdk_examples::GetPosition::Response &res)
{
  uint8_t dxl_error = 0;
  int dxl_comm_result = COMM_TX_FAIL;
  
  uint16_t pos = 0;

  dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, (uint8_t)req.id, ADDR_PRESENT_POSITION, &pos, &dxl_error);
  ROS_INFO("getPosition : [ID:%d] -> [POSITION:%d]", req.id, pos);

  res.position = pos;
  return true;
}

void setPositionCallback(const dynamixel_sdk_examples::SetPosition::ConstPtr &msg)
{

  ROS_INFO("Setting Position");

  uint8_t dxl_error = 0;
  
  uint16_t pos = (unsigned int)msg->position;

  packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_GOAL_POSITION, pos, &dxl_error);
  ROS_INFO("setPosition : [ID:%d] [POSITION:%d]", msg->id, msg->position);
}

void turnLEDonOff (const dynamixel_sdk_examples::SetPosition::ConstPtr &msg)
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

void movingSpeed (const dynamixel_sdk_examples::SetPosition::ConstPtr &msg)
{
  ROS_INFO("Speed");
  uint8_t dxl_error = 0;
  uint16_t sp = (unsigned int)msg->speed;
  packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_MOVING_SPEED, sp, &dxl_error);
  ROS_INFO("New Speed");
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
  ros::Subscriber set_position_sub = nh.subscribe("/set_position", 10, setPositionCallback);
  ros::ServiceServer get_position_srv = nh.advertiseService("/get_position", getPresentPosition);
  ros::Subscriber set_speed_sub = nh.subscribe("/set_speed", 10, movingSpeed);
  ros::Subscriber led_sub = nh.subscribe("/led", 10, turnLEDonOff);


  while (ros::ok())
  {
    usleep(8 * 1000);

    ros::spin();
  }

  return 0;
}
