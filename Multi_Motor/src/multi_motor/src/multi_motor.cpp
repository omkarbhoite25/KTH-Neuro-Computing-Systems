// Name: Omkar Bhoite
// Project: Robotics Head
// Advised and Guided by: Prof. Jorg Conradt & Juan Pablo Romero Bermudez

/*******************************************************************************
 * Open terminal #1
 * $ roscore
 * 
 * Open terminal #2
 * $ rosrun multi_motor multi_motor
 * 
 * Open terminal #3 (run one of below commands at a time to explore how the motors in the robot head can be controlled)
 * $ rostopic pub -1 /{rostopic name} multi_motor/Control "{position: 0}"
 * $ rosservice call /get_position "id: 1"

*******************************************************************************/

#include <ros/ros.h>

#include "std_msgs/String.h"
#include "multi_motor/GetPosition.h"
#include "multi_motor/Control.h"
#include </opt/ros/noetic/include/dynamixel_sdk/dynamixel_sdk.h>
#include<cmath>
using namespace dynamixel;

// Control table address
#define ADDR_TORQUE_ENABLE    24
#define ADDR_GOAL_POSITION    30
#define ADDR_PRESENT_POSITION 36
#define ADDR_LED              25
#define ADDR_MOVING_SPEED     32
#define ADDR_TORQUE            34  

// Protocol version
#define PROTOCOL_VERSION      1.0             // Default Protocol version of DYNAMIXEL X series.

// Default setting
#define DXL1_ID               1               // DXL1 ID - Base motor of the head for left-right movement (head_lr)
#define DXL2_ID               2               // DXL2 ID - Motor corresponding head movement up-down (head_ud)
#define DXL3_ID               3               // DXL3 ID - Motor corresponding eye movement left-right (reye_lr)
#define DXL4_ID               4               // DXL4 ID - Motor corresponding eye movement left-right (leye_lr)
#define DXL5_ID               5               // DXL5 ID - Motor corresponding eye movement up-down (reye_ud)
#define DXL6_ID               6               // DXL6 ID - Motor corresponding eye movement up-down (leye_ud)
#define BAUDRATE              1000000           // Default Baudrate of DYNAMIXEL X series
#define DEVICE_NAME           "/dev/ttyACM0"  // [Linux] To find assigned port, use "$ ls /dev/tty*" command

PortHandler *portHandler;
PacketHandler *packetHandler;

// To get the current position of the motor

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

// Function to talk to motor so as to ask them to move to a desired position.

void talkToMotor(int id, const multi_motor::Control::ConstPtr &msg)
{
  ROS_INFO("Setting Position");
  uint8_t dxl_error = 0;
  uint16_t pos = (unsigned int)msg->position;
  packetHandler->write2ByteTxRx(portHandler, id, ADDR_GOAL_POSITION, pos, &dxl_error);
}

void setPositionCallback1(const multi_motor::Control::ConstPtr &msg)
{
  uint16_t posi = (unsigned int)msg->position;
  if (posi<1500)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, 1500, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 1500",posi);
  }
  else if (posi>2500)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, 2500, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2500",posi);
  }
  else
  {
    talkToMotor(DXL1_ID, msg);
    ROS_INFO("Setting the position of motor 1");
    ROS_INFO(" Setting it to [%d] position",posi);
  }
}

// Function to move the head up-down (head_ud)
void setPositionCallback2(const multi_motor::Control::ConstPtr &msg)
{
  uint16_t posi = (unsigned int)msg->position;
  if (posi<2000)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, 2000, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2000",posi);
  }
  else if (posi>2900)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, 2900, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2900",posi);
  }
  else
  {
    talkToMotor(DXL2_ID, msg);
    ROS_INFO("Setting the position of motor 2");
    ROS_INFO(" Setting it to [%d] position",posi);
  }
}

// Function to move the right eye left-right (reye_lr)
void setPositionCallback3(const multi_motor::Control::ConstPtr &msg)
{
  uint16_t posi = (unsigned int)msg->position;
  if (posi<1500)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL3_ID, ADDR_GOAL_POSITION, 1500, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 1500",posi);
  }
  else if (posi>2500)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL3_ID, ADDR_GOAL_POSITION, 2500, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2500",posi);
  }
  else
  {
    talkToMotor(DXL3_ID, msg);
    ROS_INFO("Setting the position of motor 3");
    ROS_INFO(" Setting it to [%d] position",posi);
  }
}

// Function to move the left eye left-right (leye_lr)
void setPositionCallback4(const multi_motor::Control::ConstPtr &msg)
{
  uint16_t posi = (unsigned int)msg->position;
  if (posi<1500)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, 1500, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 1500",posi);
  }
  else if (posi>2500)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, 2500, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2500",posi);
  }
  else
  {
    talkToMotor(DXL4_ID, msg);
    ROS_INFO("Setting the position of motor 4");
    ROS_INFO(" Setting it to [%d] position",posi);
  }
}

// Function to move the right eye up-down (reye_ud)
void setPositionCallback5(const multi_motor::Control::ConstPtr &msg)
{
  uint16_t posi = (unsigned int)msg->position;
  if (posi<1700)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL5_ID, ADDR_GOAL_POSITION, 1700, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 1700",posi);
  }
  else if (posi>2300)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL5_ID, ADDR_GOAL_POSITION, 2300, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2300",posi);
  }
  else
  {
    talkToMotor(DXL5_ID, msg);
    ROS_INFO("Setting the position of motor 5");
    ROS_INFO(" Setting it to [%d] position",posi);
  }
}

// Function to move the left eye up-down (leye_ud)
void setPositionCallback6(const multi_motor::Control::ConstPtr &msg)
{
  uint16_t posi = (unsigned int)msg->position;
  if (posi<1700)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL6_ID, ADDR_GOAL_POSITION, 1700, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 1700",posi);
  }
  else if (posi>2300)
  {
    uint8_t dxl_error = 0;
    packetHandler->write2ByteTxRx(portHandler, DXL6_ID, ADDR_GOAL_POSITION, 2300, &dxl_error);
    ROS_INFO("Sorry wrong value [%d] setting it to default position 2300",posi);
  }
  else
  {
    talkToMotor(DXL6_ID, msg);
    ROS_INFO("Setting the position of motor 6");
    ROS_INFO(" Setting it to [%d] position",posi);
  }
}

// Function to turn led on-off for any given motor

void turnLEDonOff (const multi_motor::Control::ConstPtr &msg)
{
  for (int i=0; i<=5; i++)
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

// Function to change the speed of the motor.

void movingSpeed (const multi_motor::Control::ConstPtr &msg)
{
  ROS_INFO("Setting new speed");
  uint8_t dxl_error = 0;
  uint16_t sp = (unsigned int)msg->speed;
  packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_MOVING_SPEED, sp, &dxl_error);
  ROS_INFO("New speed set for motor %d", (uint8_t)msg->id); 
}


// Function to change the torque of the motor.
void setTorque (const multi_motor::Control::ConstPtr &msg)
{
  ROS_INFO("Setting new torque");
  uint8_t dxl_error = 0;
  uint16_t tor = (unsigned int)msg->torque;
  packetHandler->write2ByteTxRx(portHandler, (uint8_t)msg->id, ADDR_TORQUE, tor, &dxl_error);
  ROS_INFO("New torque set for motor %d",(uint8_t)msg->id );
}

// A function to communicate with motor
void communiateWithMotor(int id, int add, int value)
{
  uint8_t dxl_error = 0;
  packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);
  packetHandler->write2ByteTxRx(portHandler, id, add, value, &dxl_error);
}

// To make sure that the robot head is set to the default position as per its structure.

void settingHeadToDefaultPosition()
{
  
  // Lower the speed of motors to take safety into account
  communiateWithMotor(DXL1_ID,ADDR_MOVING_SPEED,50);
  communiateWithMotor(DXL2_ID,ADDR_MOVING_SPEED,50);
  communiateWithMotor(DXL3_ID,ADDR_MOVING_SPEED,50);
  communiateWithMotor(DXL4_ID,ADDR_MOVING_SPEED,50);
  communiateWithMotor(DXL5_ID,ADDR_MOVING_SPEED,50);
  communiateWithMotor(DXL6_ID,ADDR_MOVING_SPEED,50);

  // Moving the motors to default positions
  communiateWithMotor(DXL1_ID,ADDR_GOAL_POSITION,2000);
  communiateWithMotor(DXL2_ID,ADDR_GOAL_POSITION,2450);
  communiateWithMotor(DXL3_ID,ADDR_GOAL_POSITION,2000);
  communiateWithMotor(DXL4_ID,ADDR_GOAL_POSITION,2000);
  communiateWithMotor(DXL5_ID,ADDR_GOAL_POSITION,2000);
  communiateWithMotor(DXL6_ID,ADDR_GOAL_POSITION,2000);
}


// Function is use to enable torque for all the motors in the robotic head
void enableTorque()
{
  communiateWithMotor(DXL1_ID,ADDR_TORQUE_ENABLE,1);
  communiateWithMotor(DXL2_ID,ADDR_TORQUE_ENABLE,1);
  communiateWithMotor(DXL3_ID,ADDR_TORQUE_ENABLE,1);
  communiateWithMotor(DXL4_ID,ADDR_TORQUE_ENABLE,1);
  communiateWithMotor(DXL5_ID,ADDR_TORQUE_ENABLE,1);
  communiateWithMotor(DXL6_ID,ADDR_TORQUE_ENABLE,1);
}

// Main Function
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
  //Setting head to default position
  settingHeadToDefaultPosition();

  // To Enable torque
  enableTorque();
 
// Create rostopics
  ros::Subscriber set_position1_sub = nh.subscribe("/head_lr", 10, setPositionCallback1);
  ros::Subscriber set_position2_sub = nh.subscribe("/head_ud", 10, setPositionCallback2);
  ros::Subscriber set_position3_sub = nh.subscribe("/reye_lr", 10, setPositionCallback3);
  ros::Subscriber set_position4_sub = nh.subscribe("/leye_lr", 10, setPositionCallback4);
  ros::Subscriber set_position5_sub = nh.subscribe("/reye_ud", 10, setPositionCallback5);
  ros::Subscriber set_position6_sub = nh.subscribe("/leye_ud", 10, setPositionCallback6);
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
