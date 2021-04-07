import rospy
import sys
import os
import time
from multiprocessing import Process
from dynamixel_sdk_examples.msg import SetPosition
# from dynamixel_sdk_examples.msg import SetLed
from dynamixel_sdk_examples.srv import GetPosition

rospy.init_node("whatever")
print("Hi")
motor1Pos = rospy.Publisher("/set_position", SetPosition, queue_size=1)
motor2Pos = rospy.Publisher("/set_position", SetPosition, queue_size=1)
# motorSpeed
rospy.loginfo("%s started" % rospy.get_name())

os.system("rostopic pub -1 /set_position dynamixel_sdk_examples/SetPosition '{id: 1,position: 2000}'")
os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 1,speed: 50}'")
os.system("rostopic pub -1 /set_position dynamixel_sdk_examples/SetPosition '{id: 2,position: 2450}'")
os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 2,speed: 50}'")
delta = 5

moment_cmd = SetPosition()

def motor1():
    moment_cmd.id =  1
    max_yaw = 3000 
    min_yaw = 1000
    moment_cmd.position =  max_yaw
    motor1Pos.publish(moment_cmd)
    time.sleep(delta)


    moment_cmd.position =  min_yaw
    motor1Pos.publish(moment_cmd)
    time.sleep(delta)


    moment_cmd.position =  max_yaw-min_yaw
    motor1Pos.publish(moment_cmd)
    time.sleep(delta)
    print("hi")
#########################################################################
def motor2():
    moment_cmd.id = 2 
    moment_cmd.position =  2000
    motor2Pos.publish(moment_cmd)
    time.sleep(delta)

if __name__=='__main__':
    p1 = Process(target = motor1)
    p1.start()
    p2 = Process(target = motor2)
    p2.start()
    p1.join()
    p2.join()

print('Publishing')
rospy.spin()