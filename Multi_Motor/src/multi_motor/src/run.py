import rospy
import sys
import os
import time
from multiprocessing import Process
from multi_motor.msg import Control
# from multi_motor.msg import SetLed
from multi_motor.srv import GetPosition

rospy.init_node("whatever")
print("Hi")
motorPos1 = rospy.Publisher("/set_position1", Control, queue_size=1)
motorPos2 = rospy.Publisher("/set_position2", Control, queue_size=1)
motorPos3 = rospy.Publisher("/set_position3", Control, queue_size=1)
motorPos4 = rospy.Publisher("/set_position4", Control, queue_size=1)
motorPos5 = rospy.Publisher("/set_position5", Control, queue_size=1)
motorPos6 = rospy.Publisher("/set_position6", Control, queue_size=1)

# # motorSpeed
rospy.loginfo("%s started" % rospy.get_name())
# os.system("rostopic pub -1 /set_position1 multi_motor/Control '{position: 1500}'")
os.system("rostopic pub -1 /set_speed multi_motor/Control '{id: 1,speed: 40}'")
# os.system("rostopic pub -1 /set_position2 multi_motor/Control '{position: 2450}'")
os.system("rostopic pub -1 /set_speed multi_motor/Control '{id: 2,speed: 40}'")
# os.system("rostopic pub -1 /set_position3 multi_motor/Control '{position: 2000}'")
os.system("rostopic pub -1 /set_speed multi_motor/Control '{id: 3,speed: 40}'")
# os.system("rostopic pub -1 /set_position4 multi_motor/Control '{position: 2000}'")
os.system("rostopic pub -1 /set_speed multi_motor/Control '{id: 4,speed: 40}'")
# os.system("rostopic pub -1 /set_position5 multi_motor/Control '{position: 2000}'")
os.system("rostopic pub -1 /set_speed multi_motor/Control '{id: 5,speed: 40}'")
# os.system("rostopic pub -1 /set_position6 multi_motor/Control '{position: 2000}'")
os.system("rostopic pub -1 /set_speed multi_motor/Control '{id: 6,speed: 40}'")
delta = 3
time.sleep(delta)
moment_cmd = Control()

max_yaw = 3000 
min_yaw = 1000


moment_cmd.position = 2000
motorPos1.publish(moment_cmd)

moment_cmd.position =  1500
motorPos1.publish(moment_cmd)

moment_cmd.position = 2000
motorPos5.publish(moment_cmd)

moment_cmd.position = 2000
motorPos6.publish(moment_cmd)

moment_cmd.position = 2000
motorPos5.publish(moment_cmd)

moment_cmd.position = 2000
motorPos6.publish(moment_cmd)

time.sleep(delta)

moment_cmd.position = 1000
motorPos1.publish(moment_cmd)

moment_cmd.position =  max_yaw
motorPos1.publish(moment_cmd)

moment_cmd.position = 1500
motorPos5.publish(moment_cmd)

moment_cmd.position = 2500
motorPos6.publish(moment_cmd)

moment_cmd.position = 1500
motorPos5.publish(moment_cmd)

moment_cmd.position = 2500
motorPos6.publish(moment_cmd)

time.sleep(delta)


moment_cmd.position = 2000
motorPos1.publish(moment_cmd)

moment_cmd.position =  min_yaw
motorPos1.publish(moment_cmd)


moment_cmd.position = 2000
motorPos5.publish(moment_cmd)

moment_cmd.position = 2000
motorPos6.publish(moment_cmd)

moment_cmd.position = 2500
motorPos5.publish(moment_cmd)

moment_cmd.position = 1500
motorPos6.publish(moment_cmd)

time.sleep(delta)

moment_cmd.position = 3000
motorPos1.publish(moment_cmd)

moment_cmd.position =  max_yaw - min_yaw
motorPos1.publish(moment_cmd)

moment_cmd.position = 2500
motorPos5.publish(moment_cmd)

moment_cmd.position = 1500
motorPos6.publish(moment_cmd)

moment_cmd.position = 1500
motorPos5.publish(moment_cmd)

moment_cmd.position = 2500
motorPos6.publish(moment_cmd)

time.sleep(delta)



moment_cmd.position = 2000
motorPos1.publish(moment_cmd)


moment_cmd.position =  max_yaw
motorPos1.publish(moment_cmd)

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