#!/usr/bin/env python
"""
=================================================
rosSim.py - ROS/Gazebo Initialization Handler
=================================================
"""

import sys, subprocess, os, execute, time, os, shutil

class initHandler:
    def __init__(self, proj, calib=False):
	run = False

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
	temp = os.path.join(root,'gazebo_worlds')
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
			run = True	
	                time.sleep(1)
	                break

    def getSharedData(self):
        # TODO: Return a dictionary of any objects that will need to be shared with
        # other handlers
        return {}
