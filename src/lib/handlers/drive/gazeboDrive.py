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
         	except NameError:
             		print "(DRIVE) Locomotion Command Handler not found."
			exit(-1)
   		self.turning = False 

     	def setVelocity(self, x, y, theta=0):
		#TODO:  THis is currently not working correctly.  Not sure the issue.  
		#       Have tried tons of variations on the checking when turning and when not
		#       It seems to work but only the pr2 turns so slowly that you cant really run
		#       A simulation.  Have tried multiply the angular vel by huge nums and doesn't seem to help

		twist = Twist().
   		velangle = math.atan2(y,x)   math.pi/2
   		rel_heading = theta-velangle
   		rel_heading = math.atan2(math.sin(rel_heading),math.cos(rel_heading))  

   		
		if (not self.turning and abs(rel_heading) > math.pi/6):
     			self.turning = True    
     			#print "not turning"
   		if (self.turning) :    
     			twist.angular.z = -3 * cmp (rel_heading,0)
     			twist.linear.x = 0
  			twist.linear.y =0
     			#print "turning"  

   		else:
     			#print "going straight"
     			twist.angular.z = 0
     			twist.linear.x = x
     			twist.linear.y = y

 		self.loco.sendCommand(twist)
