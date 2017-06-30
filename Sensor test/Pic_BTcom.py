from ePuck import ePuck
from ePuckUtil import *
import sys
import re
import cv2
import time

try:
	mac = epucks['3674']
 	robot = ePuck(mac,debug=True)
	robot.connect()
	msg = robot.send_and_receive('V\n')
	print msg
	msg = robot.send_and_receive('V\n')
	print msg
	msg = robot.send_and_receive('V\n')
	print msg
	msg = robot.send_and_receive('V\n')
	print msg

	cv2.namedWindow('test', 1)
	robot.enable('camera')
	robot.set_camera_parameters('RGB_365', 40, 40, 1)
	while(1):
		robot.step()
		image = robot.get_image()
		print 'image: ',image
		robot.show_image('test')


except KeyboardInterrupt:
	print '\n'
	log('Stoping the robot. Bye!')
	for robot in robotlist:
		robot.close()
	sys.exit()
except Exception, e:
	error(e)
	sys.exit(1)

