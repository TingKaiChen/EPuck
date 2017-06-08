from ePuck import ePuck
from ePuckUtil import *
import sys
import re
import curses
import time


def main(macs, robot_ids):

	log('Connecting with the ePuck')
	try:
		# First, create an ePuck object.
		# If you want debug information:
		#~ robot = ePuck(mac, debug = True)
		# else:
		robotlist = []

		for mac in macs:
			robot = ePuck(mac,debug=False)
			# Second, connect to it
			robot.connect()
			# You can enable various sensors at the same time. Take a look to
			# to DIC_SENSORS for know the name of the sensors
			robot.enable('proximity')
			robotlist.append(robot)

		log('Conection complete. CTRL+C to stop')
		log('Library version: ' + robot.version)

	except Exception, e:
		error(e)
		sys.exit(1)

	try:
		matrix = ( (150, -35), (100, -15), (80, -10), (-10, -10),
        (-10, -10), (-10, 80), (-30, 100), (-20, 150) )
		while True:
			# Important: when you execute 'step()', al sensors
			# and actuators are updated. All changes you do on the ePuck
			# will be effectives after this method, not before
			for robot in robotlist:
				robot.step()

				# Now, we can get updated information from the sensors
				prox_sensors = robot.get_proximity()

				# The Braitenberg algorithm is really simple, it simply computes the
				# speed of each wheel by summing the value of each sensor multiplied by
				# its corresponding weight. That is why each sensor must have a weight
				# for each wheel.
				wheels = [0, 0]
				for w, s in ((a, b) for a in range(len(wheels)) for b in range(len(prox_sensors))):
					# We need to recenter the value of the sensor to be able to get
					# negative values too. This will allow the wheels to go
					# backward too.
					wheels[w] += matrix[s][w] * (1.0 - (prox_sensors[s] / 512))

				# Now, we set the motor speed. Remember that we need to execute 'step()'
				# for make this command effective
				robot.set_motors_speed(wheels[0], wheels[1])

	except KeyboardInterrupt:
		log('Stoping the robot. Bye!')
		for robot in robotlist:
			robot.close()
		sys.exit()
	except Exception, e:
		print e

	return 0

if __name__ == '__main__':
	X = '([a-fA-F0-9]{2}[:|\-]?){6}'
	if len(sys.argv) < 2:
		error("Usage: " + sys.argv[0] + "Multiple ePuck_ID | MAC Address")
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

