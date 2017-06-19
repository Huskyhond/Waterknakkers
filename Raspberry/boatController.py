from Control import *
from followQuay import *
from followCoords import *
import sys, json, math
from time import sleep

print('Running boat Controller')
c = Controller()

driveValues = [0,0,0]
def driveBoat(leftEngine, rightEngine, rudder):
	driveValues = [leftEngine, rightEngine, rudder]
	c.driveBoat(leftEngine, rightEngine, rudder)

max_power = 50

followQuay = False
sensorAngle = 45
fq = Follow(driveBoat,max_power,sensorAngle,20) # driveBoat Callback, setsensorValues callback, max_power, sensorAngle, temperature, debug

followCoords = False
goal = [51,60] # The goal coordinates
fc = Coords(driveBoat,max_power,goal,False) # driveBoat Callback, max_power, goal, debug

print(json.dumps({'controllable': c.controllable, 'followQuay': fq.running, 'followCoords' : fc.running, 'sensorDistances' : fq.pings, 'driveValues' : driveValues }))
sys.stdout.flush()

while True:
	# Wait for input from NodeJS
	userinput = sys.stdin.readline()
	if(not c.connected):
		print("Trying to reconnect with Arduino")
		c = Controller()
		sleep(0.5)
		continue

	# If the length is more than 1, NodeJS Pushes an empty string time to time and also one character time to time.
	if(len(userinput) > 1):
		# Parse to python json object (list)
		jsonObj = json.loads(userinput)
		# Put values in correct variables
		if len(jsonObj) == 1:
			temp = jsonObj[0]
			if not fq.running:
				fq = Follow(driveBoat,max_power,sensorAngle,temp)
			continue

		# Parse json data from web client
		engineLeft = jsonObj[0]
		engineRight = jsonObj[1]
		rudder = jsonObj[2]
		if len(jsonObj) > 3:
			followQuay = jsonObj[3]

		# If controllable send data to arduino.
		if c.controllable:
			# Start following the quay wall
			if followQuay and not fq.running and not followCoords and not fc.running:
				fq.start()
			# Stop following the quay wall and stop motor and rudder
			elif not followQuay and fq.running:
				fq.stop()
				driveBoat(0,0,0)
			# Start following coordinates
			elif not followQuay and not fq.running and not fc.running and followCoords:
				fc.start()
			# Stop following coordinates and stop motor and rudder
			elif fc.running and not followCoords:
				fc.stop()
				driveBoat(0,0,0)
			# Drive the boat using user controls
			elif not followQuay and not fq.running and not fc.running and not followCoords:
				# Trying to write data to arduino.
				driveBoat(engineLeft,engineRight,rudder)
		else:
			# Checks if still uncontrollable.
			c.check()
			# Stop the follow quay wall or follow coords thread if boat is not controllable
			if fq.running:
				fq.stop()
			if fc.running:
				fc.stop()

		if followCoords and not fc.running:
			followCoords = False

		print(json.dumps({'controllable': c.controllable, 'followQuay': fq.running, 'followCoords' : fc.running, 'sensorDistances' : fq.pings, 'driveValues' : driveValues }))

	sys.stdout.flush()
