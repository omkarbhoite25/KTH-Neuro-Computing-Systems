# KTH-Neuro-Computing-Systems (Project: Robotic Head)
* Project by: Omkar Vilas Bhoite
* Advised and Guided by: Prof. Jorg Conradt & Juan Pablo Romero Bermudez

# #########################################################################################################################################################################################

# #########################################################################################################################################################################################

#### Steps to run the robotics head using ros topics and services.

###### [1]. Downlaod the Dynamixel SDK from https://github.com/ROBOTIS-GIT/DynamixelSDK.git and install the one for ros version. Or the shortest way to install library is by using the following command. (Make sure to put the correct ROS-DISTRO.)
```
$ sudo apt-get install ros-{$ros_distro}-dynamixel-sdk*
```
###### [2]. Clone this repository.
###### [3]. Open the file named multi_motor.cpp in Multi_Motor and provide the path to the dynamixel library installed on you computer. The path maybe similar to like one I use but your distro might be different. (Look for #include </opt/ros/noetic/include/dynamixel_sdk/dynamixel_sdk.h> and update it with your path)

###### Path on my computer
```
/opt/ros/noetic/include/dynamixel_sdk
```
###### For your computer it maybe
```
/opt/ros/{$ros_distro}/include/dynamixel_sdk
```

###### Also, make sure to check for the USB port and add the following in to the .cpp file. You can check to which port you are connected to using following command. (Look for #define DEVICE_NAME           "/dev/ttyACM0" and change  the port as per your port name, it maybe USB* or ACM*)
```
$ ls /dev/tty*
```
###### If serial port is not opening then there is chance that the user is not added to the dialout group, and to add user to dialout group use the following command (this is optional, just in case you are not able to open the port)

```
$ sudo usermod -a -G dialout <username>
```

###### Now we need to make sure that we have access to the port and for that we need to give the port acccess to read and write, and to achieve that us the following command. Where the asterick in " /dev/tty* " corresponds to USB or ACM which you can verify using the above command. 

```
$ sudo chmod a+rw /dev/tty*
```


###### [4]. Perform the following command to build the files for the robotic head

```
$ cd Multi_Motor/
$ catkin_make
$ source devel/setup.bash
```

###### [5]. Open 3 new terminals. (Make sure that you are in the same folder where you performed the step 3)
###### [6]. In first terminal execute the following command 

```
$ source devel/setup.bash
$ roscore
```
###### [7]. In the second termianl execute the following command 
```
$ source devel/setup.bash
$ rosrun multi_motor multi_motor
```
###### [8]. In the third termianl execute the following command

```
$ source devel/setup.bash
$ python3 src/multi_motor/src/run.py
```
# #########################################################################################################################################################################################

### NOTE

# #########################################################################################################################################################################################


###### Note : You can also eliminate retyping the "$ source devel/setup.bash" command, by adding it in the .bashrc file. To do so you need to follow the commands
###### Open the .bashrc file. Since, I'm using vscode I will follow the following command

```
$ code ~/.bashrc
```

###### and paste the following command at the bottom of the file 

```
source ~/KTH-Neuro-Computing-Systems/Multi_Motor/devel/setup.bash
```
###### Once, it is done you need to restart the terminal, and follow the procedure to run the scripts.


