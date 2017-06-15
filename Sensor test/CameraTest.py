#!/usr/local/bin python
# -*- coding: utf-8 -*-
#
#       line_follower.py
#
#       Copyright 2010 Manuel Martín Ortiz <manuel.martin@itrblabs.eu>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

#		-- Photo Taker --
#
#		Simple program to take pictures of the camera while turning on itself
#

from ePuck import ePuck
from ePuckUtil import *
import sys
import re
import time
import cv2
import numpy as np


def main(macs,robot_ids):
	global_speed = 180
	fs_speed = 0.6
	threshold = 1000

	window_name= 'image'

	print('Connecting with the ePuck')
	try:
		# First, create an ePuck object.
		# If you want debug information:
		# ~ robot = ePuck(mac, debug = True)
		# ele:
		robotlist = []
		winNum = 0

		for mac in macs:
			robot = ePuck(mac,debug = False)
			# Second, connect to it
			robot.connect()
			# You can enable various sensors at the same time. Take a look to
			# to DIC_SENSORS for know the name of the sensors
			robot.enable('camera')
			# We have to set the camera parameters
			robot.set_camera_parameters('LINEAR_CAM', 40, 40, 8)
			robotlist.append(robot)
			cv2.namedWindow('Robot_'+str(winNum), 1)
			cv2.moveWindow('Robot_'+str(winNum), winNum%3*500, winNum/3*500)
			winNum += 1

		log('Conection complete. CTRL+C to stop')
		log('Library version: ' + robot.version)

	except Exception, e:
		error(e)
		sys.exit(1)

	try:
		counter = 0
		
		while True:
			# Important: when you execute 'step()', al sensors
			# and actuators are updated. All changes you do on the ePuck
			# will be effectives after this method, not before
			starttime = time.time()
			t = 0
			winNum = 0
			for robot in robotlist:
				robot.step()

				image = robot.get_image()

				if image != None:
					# Do something with the image
					t += time.time()-starttime
					robot.show_image('Robot_'+str(winNum))
					winNum += 1
					counter += 1
				else:
					log('No image received!')
				starttime = time.time()
			if t != 0:
				print "Average image rate: ", 1./t,'fps'

	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		print '\n'
		log('Stoping the robot. Bye!')
		for robot in robotlist:
			robot.close()
		sys.exit()
	except Exception, e:
		error(e)

	return 0


if __name__ == '__main__':
	print cv2.__version__
	X = '([a-fA-F0-9]{2}[:|\-]?){6}'
	if len(sys.argv) < 2:
		error("Usage: " + sys.argv[0] + " ePuck_ID | MAC Address")
		sys.exit()
	robot_ids = sys.argv[1:]

	macs=[]
	all_flag = False
	if '-all' in robot_ids:
		# Connect all 6 e-Puck robots
		all_flag = True
		macs = epucks.values()
		robot_ids = epucks.keys()
	else:
		for robot_id in robot_ids:
			if epucks.has_key(robot_id):
				macs.append(epucks[robot_id])
			elif re.match(X,robot_id) != 0 and len(robot_id) != 4:
				macs.append(epucks[robot_id])
			else:
				error('Incorrect Mac direction or ID: '+robot_id)
				quit()

	main(macs,robot_ids)
