import sys
import collections

# You can use this dictionary to asociate an ePuck ID with its MAC Address
epucks = {
	'3419' : '10:00:E8:D7:03:D0',	
	'3428' : '10:00:E8:D7:03:D4',	
	'3624' : '10:00:E8:D7:03:C2',
	'3672' : '10:00:E8:D7:03:C8',	
	'3673' : '10:00:E8:D7:03:AF',	
	'3674' : '10:00:E8:D7:03:B1',	
}
epucks = collections.OrderedDict(sorted(epucks.items()))

def log(text):
	"""	Show @text in standart output with colors """

	blue = '\033[1;34m'
	off = '\033[1;m'

	print(''.join((blue, '[Log] ', off, str(text))))

def error(text):
	red = '\033[1;31m'
	off = '\033[1;m'

	print(''.join((red, '[Error] ', off, str(text))))

def samelinePrint(stdscr,text,botIDs = [],setlineRow = False):
	# text = str(text)
	# sys.stdout.write("\r100%\033[K\r")
	# sys.stdout.write(text)
	# sys.stdout.flush()

	if setlineRow != False:
		stdscr.addstr(setlineRow, 0, text)	
		stdscr.refresh()
		return
	
	for i in xrange(len(text)):
		line = '({0[0]:>5},{0[1]:>5},{0[2]:>5},{0[3]:>5},\
{0[4]:>5},{0[5]:>5},{0[6]:>5},{0[7]:>5})'.format(text[i])
		line = 'e-Puck '+botIDs[i]+': '+line

		stdscr.addstr(i, 0, line)
	stdscr.refresh()

	