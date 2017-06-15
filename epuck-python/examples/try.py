import time

while True:
	st = time.time()
	time.sleep(2)
	et = time.time()
	print 1./(et-st)