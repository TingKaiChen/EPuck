from ePuck import ePuck
from ePuckUtil import *
import sys
import re



def main(mac):

	log('Connecting with the ePuck')
	try:
		# First, create an ePuck object.
		# If you want debug information:
		#~ robot = ePuck(mac, debug = True)
		# else:
		robot = ePuck(mac,debug=False)

		# Second, connect to it
		robot.connect()

		# You can enable various sensors at the same time. Take a look to
		# to DIC_SENSORS for know the name of the sensors
		robot.enable('proximity')

		log('Conection complete. CTRL+C to stop')
		log('Library version: ' + robot.version)

	except Exception, e:
		error(e)
		sys.exit(1)

	try:
		while True:
			robot.step()
			prox_sensors = robot.get_proximity()
			samelinePrint(str(prox_sensors))
	except KeyboardInterrupt:
		log('Stoping the robot. Bye!')
		robot.close()
		sys.exit()
	except Exception, e:
		print e

	return 0

if __name__ == '__main__':
	X = '([a-fA-F0-9]{2}[:|\-]?){6}'
	if len(sys.argv) < 2:
		error("Usage: " + sys.argv[0] + " ePuck_ID | MAC Address")
		sys.exit()
	robot_id = sys.argv[1]

	if epucks.has_key(robot_id):
		main(epucks[robot_id])

	elif re.match(X, robot_id) != 0:
		main(robot_id)

	else:
		error('You have to indicate the MAC direction of the robot')

