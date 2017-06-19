from Control import *
from followQuay import *
from followCoords import *
import sys, json, math
from time import sleep


class QuayHandle:
	def __init__(self, controller, followQuay = False):
		self.followQuay = followQuay
		self.controller = controller
		self.temperature = 20
		self.instance = Follow(driveBoat, 50, 45, self.temperature) # Callback, max_power, sensorAngle, temperature
	
	def setTemperature(self, temperature):
		self.instance = Follow(driveBoat,50,45,temperature)
		self.temperature = temperature

	def updateQuayFollow(self, newFollowQuay, maxPower):
		if newFollowQuay is self.followQuay:
			return
		else:
			self.instance = Follow(driveBoat, maxPower, 45, self.temperature)	
		
		self.followQuay = newFollowQuay
		if self.followQuay:
			self.instance.start()
		else:
			self.instance.stop()
			self.controller.driveBoat(0, 0, 0)

class CoordsHandle:
	def __init__(self, controller, followCoords = False):
		self.followCoords = followCoords
		self.controller = controller
		self.instance = Coords(driveBoat,50,[50,55],False) # Callback, max_power, goal, debug
	
	def updateCoordsFollow(self, newFollowCoords, max_power, goal):
		if newFollowCoords is self.followCoords:
			return
		else:
			self.instance = Coords(driveBoat, max_power, goal, False)

		self.followCoords = newFollowCoords
		if self.followCoords:
			self.instance.start()
		else:
			self.instance.stop()
			self.controller.driveBoat(0, 0, 0)	

driveValues = [0,0,0]
def driveBoat(leftEngine, rightEngine, rudder):
	driveValues = [leftEngine, rightEngine, rudder]
	c.driveBoat(leftEngine, rightEngine, rudder)


print('Running boat Controller')
c = Controller()
quayHandle = QuayHandle(c)
coordsHandle = CoordsHandle(c)

print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'followCoords': coordsHandle.instance.running}))

sys.stdout.flush()
while True:
	# Wait for input from NodeJS
	userinput = sys.stdin.readline()
	if(not c.connected):
		c = Controller()
		sleep(0.5)
		continue

	# If the length is more than 1, NodeJS Pushes an empty string time to time and also one character time to time.
	if(len(userinput) > 1):
		# Parse to python json object (list)
		jsonObj = json.loads(userinput)

		# Put values in correct variables
		if temperature in jsonObj:
			temperature = jsonObj['temperature']

			# Temperature will be given on initialization of the connection.
			if not quayHandle.instance.running:
				# Update Quay follower instance
				quayHandle.setTemperature(temperature)
			continue

		# If controllable send data to arduino.
		if c.controllable:
			# Start following the quay wall
			if 'followQuay' in jsonObj and not coordsHandle.followCoords:
				quayHandle.updateQuayFollow(jsonObj['followQuay'], jsonObj['maxPower'])
			
			if 'followCoords' in jsonObj and not quayHandle.followQuay:
				coordsHandle.updateCoordsFollow(jsonObj['followCoords'], jsonObj['maxPower'], [jsonObj['goalLocationX'], jsonObj['goalLocationY']])
			
			if quayHandle.instance.running:
				print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'sensorDistances' : quayHandle.instance.pings, 'followCoords': coordsHandle.instance.running, 'driveValues': driveValues}))
				continue

			if coordsHandle.instance.running:
				print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'followCoords': coordsHandle.instance.running, 'driveValues': driveValues }))
				continue

			
			# Trying to write data to arduino.
			# If the engines and rudder is set.
			if 'leftEngine' in jsonObj and 'rightEngine' in jsonObj and 'rudder' in jsonObj:
				c.driveBoat(jsonObj['leftEngine'], jsonObj['rightEngine'], jsonObj['rudder'])
		else:
			# Checks if still uncontrollable.
			c.check()
			# Stop the follow quay wall thread if boat is not controllable
			if quayHandle.instance.running:
				quayHandle.updateQuayFollow(False)

			# Stop the follow coords wall thread if boat is not controllable
			if coordsHandle.instance.running:
				coordsHandle.updateCoordsFollow(False)

		print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'followCoords': coordsHandle.instance.running}))

	sys.stdout.flush()
=======
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
