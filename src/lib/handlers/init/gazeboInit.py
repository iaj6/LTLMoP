#!/usr/bin/env python
"""
=================================================
rosSim.py - ROS/Gazebo Initialization Handler
=================================================
"""
import roslib; roslib.load_manifest('gazebo')

import sys, subprocess, os, execute, time, os, shutil, rospy
from numpy import *
from gazebo.srv import *

class initHandler:
    def __init__(self, proj, calib=False):

	# copy the .png file from current directory to: 
	#/opt/ros/cturtle/stacks/simulator_gazebo/gazebo/gazebo//share/gazebo/Media/materials/textures	

	texture_dir = '/opt/ros/cturtle/stacks/simulator_gazebo/gazebo/gazebo/share/gazebo/Media/materials/textures'	
	ltlmop_path = proj.getFilenamePrefix()
	ltlmop_map_path = ltlmop_path + "_simbg.png"

	shutil.copy (ltlmop_map_path, texture_dir)
	full_pic_path = texture_dir + "/" + proj.project_basename + "_simbg.png"
	shutil.copyfile (full_pic_path, (texture_dir + "/" + 'ltlmop_map.png'))

	
	# Set ROS package path to include gazebo_worlds where the launch files are.
	root = proj.ltlmop_root
	temp = os.path.join(root, 'etc')
	temp = os.path.join(temp,'gazebo_worlds')
	ROS_PACKAGE_PATH = temp + ":" + os.getenv('ROS_PACKAGE_PATH')
	os.environ["ROS_PACKAGE_PATH"] = ROS_PACKAGE_PATH

	
	# Create a subprocess
	start = subprocess.Popen(['roslaunch', 'gazebo_worlds', 'ltlmop.launch'], stdout=subprocess.PIPE)
	start_output = start.stdout
		
        # Wait for it to fully start up
        while 1:
		input = start_output.readline()
		print input, # Pass it on
		if input == '': # EOF
	                print "(INIT) WARNING:  Gazebo seems to have died!"
	                break
		if "spawning success True" in input:	
	                time.sleep(1)
	                break
	
	if not calib :
		# Start in the center of the defined initial region
		initial_region = proj.rfiold.regions[int(proj.exp_cfg_data['InitialRegion'][0])]
		initial_region = proj.rfi.regions[proj.rfi.indexOfRegionWithName(proj.regionMapping[initial_region.name][0])]
		center = initial_region.getCenter()

		# Load the map calibration data and the region file data to feed to the simulator
		coordmap_map2lab,coordmap_lab2map = proj.getCoordMaps(proj.exp_cfg_data)
		map2lab = list(coordmap_map2lab(array(center)))

		print "Initial region name: ", initial_region.name, " I think I am here: ", map2lab, " and center is: ", center
		print proj.exp_cfg_data['Calibration'][0]

		model_state = gazebo.msg.ModelState()
		model_state.model_name = 'pr2'
		model_state.pose.position.x = map2lab[0]
		model_state.pose.position.y = map2lab[1]		

		rospy.wait_for_service('/gazebo/set_model_state')
	    	try:
			sms = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
			sms(model_state)	
		except rospy.ServiceException, e:
	       		print "Service call failed: %s"%e
	
	
    def getSharedData(self):
        # TODO: Return a dictionary of any objects that will need to be shared with
        # other handlers
        return {}
