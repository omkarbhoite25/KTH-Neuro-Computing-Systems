execute_process(COMMAND "/home/omkar/Multi_Motor/build/dynamixel_sdk/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/omkar/Multi_Motor/build/dynamixel_sdk/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
