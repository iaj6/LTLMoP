#!/usr/bin/env python
import roslib; roslib.load_manifest('gazebo')

import rospy, math
from gazebo.srv import *

from geometry_msgs.msg import Twist
"""
==================================================================
gazeboLocomotionCommand.py - Gazebo Locomotion Command Handler
==================================================================
"""

class locomotionCommandHandler:
    def __init__(self, proj, shared_data):
       	self.pub = rospy.Publisher('/base_controller/command', Twist)
	rospy.init_node('locomotionCommand')

    def sendCommand(self, cmd):
	#twist = cmd
	twist = Twist()	
	twist.linear.x = cmd[0]
	twist.linear.y = cmd[1]
	self.pub.publish(twist)
