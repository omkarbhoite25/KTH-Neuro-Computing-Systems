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
motorPos1 = rospy.Publisher("/set_position1", SetPosition, queue_size=1)
motorPos2 = rospy.Publisher("/set_position2", SetPosition, queue_size=1)
motorPos3 = rospy.Publisher("/set_position3", SetPosition, queue_size=1)
motorPos4 = rospy.Publisher("/set_position4", SetPosition, queue_size=1)
motorPos5 = rospy.Publisher("/set_position5", SetPosition, queue_size=1)
motorPos6 = rospy.Publisher("/set_position6", SetPosition, queue_size=1)

# # motorSpeed
# rospy.loginfo("%s started" % rospy.get_name())
# # os.system("rostopic pub -1 /set_position1 dynamixel_sdk_examples/SetPosition '{position: 1500}'")
# os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 1,speed: 40}'")
# # os.system("rostopic pub -1 /set_position2 dynamixel_sdk_examples/SetPosition '{position: 2450}'")
# os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 2,speed: 40}'")
# # os.system("rostopic pub -1 /set_position3 dynamixel_sdk_examples/SetPosition '{position: 2000}'")
# os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 3,speed: 40}'")
# # os.system("rostopic pub -1 /set_position4 dynamixel_sdk_examples/SetPosition '{position: 2000}'")
# os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 4,speed: 40}'")
# # os.system("rostopic pub -1 /set_position5 dynamixel_sdk_examples/SetPosition '{position: 2000}'")
# os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 5,speed: 40}'")
# # os.system("rostopic pub -1 /set_position6 dynamixel_sdk_examples/SetPosition '{position: 2000}'")
# os.system("rostopic pub -1 /set_speed dynamixel_sdk_examples/SetPosition '{id: 6,speed: 40}'")
delta = 3
time.sleep(delta)
moment_cmd = SetPosition()

max_yaw = 3000 
min_yaw = 1000


# moment_cmd.position = 2000
# motorPos1.publish(moment_cmd)

# moment_cmd.position =  1500
# motorPos1.publish(moment_cmd)

moment_cmd.position = 2000
motorPos5.publish(moment_cmd)

moment_cmd.position = 2000
motorPos6.publish(moment_cmd)

# moment_cmd.position = 2000
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 2000
# motorPos6.publish(moment_cmd)

time.sleep(delta)

# moment_cmd.position = 1000
# motorPos1.publish(moment_cmd)

# moment_cmd.position =  max_yaw
# motorPos1.publish(moment_cmd)

moment_cmd.position = 1500
motorPos5.publish(moment_cmd)

moment_cmd.position = 2500
motorPos6.publish(moment_cmd)

# moment_cmd.position = 1500
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 2500
# motorPos6.publish(moment_cmd)

time.sleep(delta)


# moment_cmd.position = 2000
# motorPos1.publish(moment_cmd)

# moment_cmd.position =  min_yaw
# motorPos1.publish(moment_cmd)


moment_cmd.position = 2000
motorPos5.publish(moment_cmd)

moment_cmd.position = 2000
motorPos6.publish(moment_cmd)

# moment_cmd.position = 2500
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 1500
# motorPos6.publish(moment_cmd)

time.sleep(delta)

# moment_cmd.position = 3000
# motorPos1.publish(moment_cmd)

# moment_cmd.position =  max_yaw - min_yaw
# motorPos1.publish(moment_cmd)

moment_cmd.position = 2500
motorPos5.publish(moment_cmd)

moment_cmd.position = 1500
motorPos6.publish(moment_cmd)

# moment_cmd.position = 1500
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 2500
# motorPos6.publish(moment_cmd)

time.sleep(delta)



# moment_cmd.position = 2000
# motorPos1.publish(moment_cmd)


# moment_cmd.position =  max_yaw
# motorPos1.publish(moment_cmd)

moment_cmd.position = 2000
motorPos5.publish(moment_cmd)

moment_cmd.position = 2000
motorPos6.publish(moment_cmd)

# moment_cmd.position = 2500
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 1500
# motorPos6.publish(moment_cmd)

# time.sleep(delta)

# speed_motor = 40

# moment_cmd.position = 2400
# motorPos2.publish(moment_cmd)

# moment_cmd.position =  min_yaw
# motorPos1.publish(moment_cmd)


# moment_cmd.position = 2500
# motorPos3.publish(moment_cmd)

# moment_cmd.position = 2500
# motorPos4.publish(moment_cmd)

# moment_cmd.position = 1500
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 2500
# motorPos6.publish(moment_cmd)

# time.sleep(delta)

# moment_cmd.position = 2450
# motorPos2.publish(moment_cmd)

# moment_cmd.position =  max_yaw - min_yaw
# motorPos1.publish(moment_cmd)

# moment_cmd.position = 2000
# motorPos3.publish(moment_cmd)

# moment_cmd.position = 2000
# motorPos4.publish(moment_cmd)

# moment_cmd.position = 2000
# motorPos5.publish(moment_cmd)

# moment_cmd.position = 2000
# motorPos6.publish(moment_cmd)

time.sleep(delta)










print('Publishing')
rospy.spin()