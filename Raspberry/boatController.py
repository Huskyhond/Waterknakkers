from Control import *
from followQuay import *
import sys, json, math
from time import sleep

print('Running boat Controller')
c = Controller()

def recMotorData(motorOne, motorTwo):
    c.Motor(motorOne, motorTwo)

def recRudderData(rudder):
    c.Rudder(rudder)

def driveBoat(driveValues):
	c.Motor(driveValues[0], driveValues[1])
	c.Rudder(driveValues[2])

followQuay = False
f = Follow(driveBoat,60,45)

print(json.dumps({'controllable': c.controllable, 'followQuay': f.running}))

sys.stdout.flush()
while True:
	# Wait for input from NodeJS
	userinput = sys.stdin.readline()
	if(not c.connected):
		c = Controller()
		continue

	# If the length is more than 1, NodeJS Pushes an empty string time to time and also one character time to time.
	if(len(userinput) > 1):
		# Parse to python json object (list)
		jsonObj = json.loads(userinput)
		# Put values in correct variables
		engineLeft = jsonObj[0]
		engineRight = jsonObj[1]
		rudder = jsonObj[2]
		#if jsonObj.length > 3:
		#	followQuay = jsonObj[3]
		# If controllable send data to arduino.
		if c.controllable:
			print('{ controllable: true }')
			# Start following the quay wall
			if followQuay and not f.running:
				f.start()
			# Stop following the quay wall
			elif not followQuay and f.running:
				f.stop()
			# Drive the boat using user controls
			elif not followQuay and not f.running:
				# Trying to write data to arduino.
				c.Motor(engineLeft, engineRight)
				c.Rudder(rudder)
		else:
			print('{ controllable: false }')
			# Checks if still uncontrollable.
			c.check()
			# Stop the follow quay wall thread if boat is not controllable
			if f.running:
				f.stop()

	sys.stdout.flush()
