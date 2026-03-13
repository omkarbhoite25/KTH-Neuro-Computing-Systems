#!/usr/bin/env python3
# Demo script: demonstrates robotic head movement sequences
# Uses native rospy publishers instead of subprocess calls

import rospy
import time
from multi_motor.msg import Control


def set_speed(pub_speed, motor_id, speed):
    """Set speed for a motor using the /set_speed topic."""
    msg = Control()
    msg.id = motor_id
    msg.speed = speed
    pub_speed.publish(msg)


def main():
    rospy.init_node("head_demo")
    rospy.loginfo("%s started" % rospy.get_name())

    # Motor position publishers
    pub_head_lr = rospy.Publisher("/head_lr", Control, queue_size=1)
    pub_head_ud = rospy.Publisher("/head_ud", Control, queue_size=1)
    pub_reye_lr = rospy.Publisher("/reye_lr", Control, queue_size=1)
    pub_leye_lr = rospy.Publisher("/leye_lr", Control, queue_size=1)
    pub_reye_ud = rospy.Publisher("/reye_ud", Control, queue_size=1)
    pub_leye_ud = rospy.Publisher("/leye_ud", Control, queue_size=1)
    pub_speed = rospy.Publisher("/set_speed", Control, queue_size=1)

    # Wait for publishers to connect
    rospy.sleep(1.0)

    # Set initial motor speeds
    for motor_id in range(1, 7):
        set_speed(pub_speed, motor_id, 40)

    delta = 3
    time.sleep(delta)

    cmd = Control()
    max_yaw = 3000
    min_yaw = 1000

    # Sequence 1: Head sweep + eyes neutral
    cmd.position = 3000
    pub_head_lr.publish(cmd)
    cmd.position = 1500
    pub_head_lr.publish(cmd)
    cmd.position = 2000
    pub_reye_ud.publish(cmd)
    cmd.position = 2000
    pub_leye_ud.publish(cmd)
    cmd.position = 2000
    pub_reye_ud.publish(cmd)
    cmd.position = 2000
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    # Sequence 2: Head opposite + eyes diverge
    cmd.position = 1000
    pub_head_lr.publish(cmd)
    cmd.position = max_yaw
    pub_head_lr.publish(cmd)
    cmd.position = 1500
    pub_reye_ud.publish(cmd)
    cmd.position = 2500
    pub_leye_ud.publish(cmd)
    cmd.position = 1500
    pub_reye_ud.publish(cmd)
    cmd.position = 2500
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    # Sequence 3: Center head + eyes converge
    cmd.position = 2000
    pub_head_lr.publish(cmd)
    cmd.position = min_yaw
    pub_head_lr.publish(cmd)
    cmd.position = 2000
    pub_reye_ud.publish(cmd)
    cmd.position = 2000
    pub_leye_ud.publish(cmd)
    cmd.position = 2500
    pub_reye_ud.publish(cmd)
    cmd.position = 1500
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    # Sequence 4: Head sweep + cross eyes
    cmd.position = 3000
    pub_head_lr.publish(cmd)
    cmd.position = max_yaw - min_yaw
    pub_head_lr.publish(cmd)
    cmd.position = 2500
    pub_reye_ud.publish(cmd)
    cmd.position = 1500
    pub_leye_ud.publish(cmd)
    cmd.position = 1500
    pub_reye_ud.publish(cmd)
    cmd.position = 2500
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    # Sequence 5: Reset eyes, sweep head
    cmd.position = 2000
    pub_head_lr.publish(cmd)
    cmd.position = max_yaw
    pub_head_lr.publish(cmd)
    cmd.position = 2000
    pub_reye_ud.publish(cmd)
    cmd.position = 2000
    pub_leye_ud.publish(cmd)
    cmd.position = 2500
    pub_reye_ud.publish(cmd)
    cmd.position = 1500
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    # Sequence 6: Full expression -- head tilt + all eyes move
    cmd.position = 2400
    pub_head_ud.publish(cmd)
    cmd.position = min_yaw
    pub_head_lr.publish(cmd)
    cmd.position = 2500
    pub_reye_lr.publish(cmd)
    cmd.position = 2500
    pub_leye_lr.publish(cmd)
    cmd.position = 1500
    pub_reye_ud.publish(cmd)
    cmd.position = 2500
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    # Return to default
    cmd.position = 2450
    pub_head_ud.publish(cmd)
    cmd.position = max_yaw - min_yaw
    pub_head_lr.publish(cmd)
    cmd.position = 2000
    pub_reye_lr.publish(cmd)
    cmd.position = 2000
    pub_leye_lr.publish(cmd)
    cmd.position = 2000
    pub_reye_ud.publish(cmd)
    cmd.position = 2000
    pub_leye_ud.publish(cmd)

    time.sleep(delta)

    rospy.loginfo("Demo sequence complete")
    rospy.spin()


if __name__ == "__main__":
    main()
