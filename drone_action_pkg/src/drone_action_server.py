#! /usr/bin/env python

import rospy
import actionlib

from std_msgs.msg import Empty
from drone_action_pkg.msg import DroneFeedback, DroneResult, DroneAction

class DroneActionClass(object):

    _feedback = DroneFeedback()
    _result = DroneResult()

    def __init__(self):

        self.takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)

        self._as = actionlib.SimpleActionServer(
            "drone_action_server",
            DroneAction,
            self.goal_callback,
            False)

        self._as.start()

    def goal_callback(self, goal):

        rate = rospy.Rate(1)

        if goal.command == "TAKEOFF":

            rospy.loginfo("Drone taking off")

            while not rospy.is_shutdown():

                self.takeoff_pub.publish(Empty())

                self._feedback.current_action = "TAKING OFF"
                self._as.publish_feedback(self._feedback)

                rate.sleep()

        elif goal.command == "LAND":

            rospy.loginfo("Drone landing")

            self.land_pub.publish(Empty())

            self._feedback.current_action = "LANDING"
            self._as.publish_feedback(self._feedback)

            self._result.finished = True

            self._as.set_succeeded(self._result)

if __name__ == '__main__':

    rospy.init_node('drone_action_server')

    DroneActionClass()

    rospy.spin()
