# KTH-Neuro-Computing-Systems

#### Steps to run the robotics head using ros topics and services.

###### 1. Downlaod the Dynamixel SDK from https://github.com/ROBOTIS-GIT/DynamixelSDK.git and install the one for ros version. 
###### 2. Clone this repository.
###### 3. Perform the following command to run the robotic head

```
$ cd Multi_Motor/
$ catkin_make
$ source devel/setup.bash
```

###### 4. Open 3 new terminals. (Make sure that you are in the same folder where you performed the step 3)
###### 5. In first terminal execute the following command 

```
$ source devel/setup.bash
$ roscore
```
###### 6. In the second termianl execute the following command 
```
$ source devel/setup.bash
$ rosrun multi_motor multi_motor
```
###### 7. In the third termianl execute the following command

```
$ source devel/setup.bash
$ python3 src/multi_motor/src/run.py
```
