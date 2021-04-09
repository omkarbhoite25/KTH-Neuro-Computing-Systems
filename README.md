# KTH-Neuro-Computing-Systems

#### Steps to run the robotics head using ros topics and services.

###### 1. Downlaod the Dynamixel SDK from https://github.com/ROBOTIS-GIT/DynamixelSDK.git and install the one for ros version. Or the shortest way is to install using the following command. Make sure to put the correct ROS-DISTRO.
```
$ sudo apt-get install ros-{$ros_distro}-dynamixel-sdk*
```
###### 2. Clone this repository.
###### 3. Open the file named multi_motor.cpp and provide the path to the dynamixel library installed on you computer.Also, make sure to check for the USB port and add the following in to the .cpp file. You can check to which port you are connected to using following command. 
```
$ ls /dev/tty*
```
###### 4. Perform the following command to build the files for the robotic head

```
$ cd Multi_Motor/
$ catkin_make
$ source devel/setup.bash
```

###### 5. Open 3 new terminals. (Make sure that you are in the same folder where you performed the step 3)
###### 6. In first terminal execute the following command 

```
$ source devel/setup.bash
$ roscore
```
###### 7. In the second termianl execute the following command 
```
$ source devel/setup.bash
$ rosrun multi_motor multi_motor
```
###### 8. In the third termianl execute the following command

```
$ source devel/setup.bash
$ python3 src/multi_motor/src/run.py
```
