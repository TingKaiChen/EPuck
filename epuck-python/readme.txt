We can control robots and receive sensor data via “E-Puck Python Library”
http://www.gctronic.com/doc/index.php/E-Puck#Software [2]
(section 2.4.3 Python)

Setup:
Required library: 
1. Pybluez (Bluetooth):*1 
https://gist.github.com/lexruee/fa2e55aab4380cf266fb
https://github.com/karulis/pybluez
2. PIL (Python Image Library)

*1 PyBluez installation
For Ubuntu 16.04
	Follow the instruction in https://gist.github.com/lexruee/fa2e55aab4380cf266fb
	1. sudo apt-get update
 	2. sudo apt-get install python-pip python-dev ipython
	3. sudo apt-get install bluetooth libbluetooth-dev
	4. sudo pip install pybluez
For MacOS
	1. git clone https://github.com/karulis/pybluez.git
	2. cd ./pybluez
	3. sudo python setup.py install

	If there is an error "objc.BadPrototypeError: Objective-C expects 1 argum… "
	(pull request #146) when running the example code:
	1. pip uninstall pybluez
	2. git clone https://github.com/karulis/pybluez.git
	3. cd ./pybluez
	4. git fetch origin pull/146/head
	5. git checkout FETCH_HEAD
	6. git checkout -b bugfix
	7. git checkout master
	8. git merge bugfix
	9. sudo python setup.py install