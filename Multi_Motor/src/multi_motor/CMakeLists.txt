################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(multi_motor)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11 -Wall -Wextra)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(catkin REQUIRED
  COMPONENTS
    roscpp
    std_msgs
    message_generation
    dynamixel_sdk
)

################################################################################
# Declare ROS messages, services and actions
################################################################################
## Generate messages in the 'msg' folder
add_message_files(
  FILES
    Control.msg
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
    GetPosition.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
    std_msgs
)

################################################################################
# Declare catkin specific configuration to be passed to dependent projects
################################################################################
catkin_package(
  CATKIN_DEPENDS
    roscpp
    std_msgs
    dynamixel_sdk
)

################################################################################
# Build
################################################################################
## Specify additional locations of header files
include_directories(
  ${catkin_INCLUDE_DIRS}
)

# Tick-based motor control node
add_executable(multi_motor src/multi_motor.cpp)
add_dependencies(multi_motor ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(multi_motor ${catkin_LIBRARIES})

# Radian-based motor control node
add_executable(multi_motor_radians src/multi_motor_radians.cpp)
add_dependencies(multi_motor_radians ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(multi_motor_radians ${catkin_LIBRARIES})

################################################################################
# Install
################################################################################
install(TARGETS multi_motor multi_motor_radians
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
