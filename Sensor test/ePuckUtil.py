import sys

# You can use this dictionary to asociate an ePuck ID with its MAC Address
epucks = {
	'1797' : '10:00:E8:6C:A2:B6',
	'1903' : '10:00:E8:6C:A1:C7',
	'3624' : '10:00:E8:D7:03:C2',
	'3672' : '10:00:E8:D7:03:C8',	
}

def log(text):
	"""	Show @text in standart output with colors """

	blue = '\033[1;34m'
	off = '\033[1;m'

	print(''.join((blue, '[Log] ', off, str(text))))

def error(text):
	red = '\033[1;31m'
	off = '\033[1;m'

	print(''.join((red, '[Error] ', off, str(text))))

def samelinePrint(stdscr,text):
	# text = str(text)
	# sys.stdout.write("\r100%\033[K\r")
	# sys.stdout.write(text)
	# sys.stdout.flush()
	
	line0 = '({0[0]:>5},{0[1]:>5},{0[2]:>5},{0[3]:>5},\
{0[4]:>5},{0[5]:>5},{0[6]:>5},{0[7]:>5})'.format(text[0])
	line1 = '({0[0]:>5},{0[1]:>5},{0[2]:>5},{0[3]:>5},\
{0[4]:>5},{0[5]:>5},{0[6]:>5},{0[7]:>5})'.format(text[1])
	stdscr.addstr(0, 0, line0)
	stdscr.addstr(1, 0, line1)
	stdscr.refresh()

	