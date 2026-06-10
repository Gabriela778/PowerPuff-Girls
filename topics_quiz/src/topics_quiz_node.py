#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(msg):
    move = Twist()
    
    dist_fata = msg.ranges[0]
    dist_stanga = msg.ranges[90]
    dist_dreapta = msg.ranges[270]

    if dist_fata > 1.0:
        move.linear.x = 0.2
        move.angular.z = 0.0
        rospy.loginfo("liber mai mult de 1 m")
    
    if dist_fata < 1.0:
        move.linear.x = 0.0
        move.angular.z = 0.5
        rospy.loginfo("obstacol in fata. robotul face stanga")
        
    if dist_dreapta < 1.0:
        move.linear.x = 0.0
        move.angular.z = 0.5
        rospy.loginfo("obstacol in dreapta. robotul face stanga")

    if dist_stanga < 1.0:
        move.linear.x = 0.0
        move.angular.z = -0.5
        rospy.loginfo("obstacol in stanga. robotul face dreapta")

    pub.publish(move)


rospy.init_node('topics_quiz_node')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

sub = rospy.Subscriber('/scan', LaserScan, callback)

rospy.spin()
