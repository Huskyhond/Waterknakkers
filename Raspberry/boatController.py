from Control import *
from followQuay import *
import sys, json, math
from time import sleep

print('Running boat Controller')
c = Controller()

followQuay = False
f = Follow(c.driveBoat,60,45,20)

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
		if len(jsonObj) ==1:
			temp = jsonObj[0]
			if not f.running:
				f = Follow(c.driveBoat,60,45,temp)
			continue

		engineLeft = jsonObj[0]
		engineRight = jsonObj[1]
		rudder = jsonObj[2]
		if len(jsonObj) > 3:
			followQuay = jsonObj[3]

		# If controllable send data to arduino.
		if c.controllable:
			# Start following the quay wall
			if followQuay and not f.running:
				f.start()
			# Stop following the quay wall
			elif not followQuay and f.running:
				f.stop()
				c.driveBoat(0,0,0)
			# Drive the boat using user controls
			elif not followQuay and not f.running:
				# Trying to write data to arduino.
				c.driveBoat(engineLeft,engineRight,rudder)
		else:
			# Checks if still uncontrollable.
			c.check()
			# Stop the follow quay wall thread if boat is not controllable
			if f.running:
				f.stop()
				
		print(json.dumps({'controllable': c.controllable, 'followQuay': f.running}))

	sys.stdout.flush()
