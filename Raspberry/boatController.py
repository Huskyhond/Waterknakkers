from Control import *
import sys, json, math
from time import sleep

print('Running boat Controller')
c = Controller()

def recMotorData(motorOne, motorTwo):
    c.Motor(motorOne, motorTwo)

def recRudderData(rudder):
    c.Rudder(rudder)

while True:
	# Wait for input from NodeJS
	userinput = sys.stdin.readline()
	if(not c.connected):
		c = Controller()
		continue
	# If the length is more than 1, NodeJS Pushes an empty string time to time and also one character time to time.
	if(len(userinput) > 1):
		print('Got user input: ' + userinput + '(' + str(len(userinput)) + ')')
		# Parse to python json object (list)
		jsonObj = json.loads(userinput)
		# Put values in correct variables
		engineLeft = jsonObj[0]
		engineRight = jsonObj[1]
		rudder = jsonObj[2]
		# If controllable send data to arduino.
		if c.controllable:
			print('{ controllable: true }')
			# Trying to write data to arduino.
			recMotorData(engineLeft, engineRight)
			recRudderData(rudder)
		else:
			print('{ controllable: false }')
			# Checks if still uncontrollable.
			c.check()

	sys.stdout.flush()
