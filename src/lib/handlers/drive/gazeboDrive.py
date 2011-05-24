#!/usr/bin/env python

from gazebo.srv import *

import math, time
from geometry_msgs.msg import Twist
"""
=======================================================
GazeboDrive.py - Gazebo Drive Handler
=======================================================

"""

class driveHandler:
    def __init__(self, proj, shared_data):
	try:
            self.loco = proj.loco_handler
            self.coordmap = proj.coordmap_lab2map
	    self.pose_handler = proj.pose_handler
        except NameError:
            print "(DRIVE) Locomotion Command Handler not found."
            exit(-1)
	self.turning = False
	
    def setVelocity(self, x, y, theta=0):
	twist = Twist()
	self.loco.sendCommand(twist)
