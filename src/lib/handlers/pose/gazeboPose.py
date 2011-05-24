#!/usr/bin/env python
import roslib; roslib.load_manifest('gazebo')

import rospy, math
from gazebo.srv import *
from numpy import *
from tf.transformations import euler_from_quaternion


"""
=======================================
gazeboPose.py - Gazebo Pose Handler
=======================================
"""

class poseHandler:
    def __init__(self, proj, shared_data):
	self.model_name = 'pr2'
    	self.relative_entity_name = 'world'
	self.last_pose = None
        
    def getPose(self,cached = False):
    	
	if not cached or self.last_pose is None:
		rospy.wait_for_service('/gazebo/get_model_state')
	    	try:
			gms = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
			resp = gms(self.model_name,self.relative_entity_name)
	   	except rospy.ServiceException, e:
	       		print "Service call failed: %s"%e
		self.pos_x = resp.pose.position.x
		self.pos_y = resp.pose.position.y
		self.or_x = resp.pose.orientation.x
		self.or_y = resp.pose.orientation.y
		self.or_z = resp.pose.orientation.z
		self.or_w = resp.pose.orientation.w
		angles = euler_from_quaternion([self.or_x, self.or_y, self.or_z, self.or_w])
		self.theta = angles[2]	
		self.last_pose = array([self.pos_x, self.pos_y, self.theta])
		print "last pose = ", self.last_pose
	return self.last_pose

