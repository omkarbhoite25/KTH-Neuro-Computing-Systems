cmake_minimum_required(VERSION 2.8.3)
project(head_automation)

find_package(catkin REQUIRED
  COMPONENTS
    rospy
    std_msgs
    message_generation
    multi_motor
)

# Custom messages
add_message_files(
  FILES
    ModeCommand.msg
    HeadState.msg
)

generate_messages(
  DEPENDENCIES
    std_msgs
)

# Python module setup
catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS
    rospy
    std_msgs
    message_runtime
    multi_motor
)

# Install Python scripts as executable nodes
catkin_install_python(PROGRAMS
  scripts/mode_manager_node.py
  scripts/event_tracking_node.py
  scripts/sequence_player_node.py
  scripts/keyboard_teleop_node.py
  scripts/scanning_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Install config and launch files
install(DIRECTORY config/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
)
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
