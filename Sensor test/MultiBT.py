from ePuck import ePuck
from ePuckUtil import *
import sys
import re
import curses
import time



def main(macs,robot_ids):
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
		# Multiple lines printing setting
		stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()

		# Time variables for the data rate
		timestart = time.time()
		timestep = timestart
		iter = 0

		while True:
			iter += 1
			sensorDatas=[]
			for robot in robotlist:
				robot.step()
				prox_sensors = robot.get_proximity()
				sensorDatas.append(prox_sensors)
			# Print sensor data
			samelinePrint(stdscr,sensorDatas,botIDs=robot_ids)
			# Print data rate
			timeend = time.time()
			stepAvg = 5/(timeend-timestep)
			allAvg = iter/(timeend-timestart)
			sAvgtext = '{:>10.2f}'.format(stepAvg)
			aAvgtext = '{:>10.2f}'.format(allAvg)
			sAvgtext += ' (iter/sec, for last 5 iterations)'
			aAvgtext += ' (iter/sec, for all iterations)'
			samelinePrint(stdscr,aAvgtext,setlineRow=len(sensorDatas)+1)
			if iter%5 == 0:
				samelinePrint(stdscr,sAvgtext,setlineRow=len(sensorDatas))
				timestep = timeend

	except KeyboardInterrupt:
		curses.echo()
		curses.nocbreak()
		curses.endwin()

		print '\n'
		log('Stoping the robot. Bye!')
		for robot in robotlist:
			robot.close()
		sys.exit()
	except Exception, e:
		print e

	return 0

if __name__ == '__main__':
	X = '([a-fA-F0-9]{2}[:|\-]?){6}'
	if len(sys.argv) < 1:
		error("Usage: " + sys.argv[0] + "Multiple ePuck_ID | MAC Address | -all")
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

