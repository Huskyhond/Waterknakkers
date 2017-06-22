from Control import *
from followQuay import *
from followCoords import *
import sys, json, math
from time import sleep

###
### Handles the Quay class updates states and feeds information.
###
class QuayHandle:
	def __init__(self, controller, followQuay = False):
		self.followQuay = followQuay # Set if it should follow quay upon initializing.
		self.controller = controller # Set controller
		# Initialize instance.
		self.instance = Follow(driveBoat, 50, 45, 20, False) # Callback, max_power, sensorAngle, temperature, debug
	
	### Get Quay Ping instance and set the temperature.
	def setTemperature(self, temperature):
		if self.instance.p is not None:
			self.instance.p.setTemperature(temperature)

	### Start quay if the state changed.
	def updateQuayFollow(self, newFollowQuay, maxPower):
		if newFollowQuay is self.followQuay:
			return
		
		self.followQuay = newFollowQuay
		# Start thread if true.
		if self.followQuay:
			self.instance.start()
		else: # Stop thread if false.
			self.instance.stop()
			self.controller.driveBoat(0, 0, 0)

###
### Handles the Coords class updates states and feeds information.
###
class CoordsHandle:
	def __init__(self, controller, followCoords = False):
		self.followCoords = followCoords
		self.controller = controller
		# Initialize instance
		self.instance = Coords(driveBoat,50,[50,55],False) # Callback, max_power, goalCoordinate, debug
	
	# Only update if different than before.
	def updateCoordsFollow(self, newFollowCoords, max_power, goal):
		if newFollowCoords is self.followCoords:
			return
		# Only start session if there are at least two points. (self + newPosition)
		elif newFollowCoords and len(goal)>1:
			self.instance = Coords(driveBoat, max_power, goal, False)

		# Update state
		self.followCoords = newFollowCoords
		# Start thread if there are at least two goals.
		if self.followCoords and len(goal)>1:
			self.instance.start()
		else: # Stop thread in any other case.
			self.instance.stop()
			# Stop the boat.
			self.controller.driveBoat(0, 0, 0)	

# The array which stores the engine and rudder values
driveValues = [0,0,0]
# The callback for followQuay and followCoords
# The callback stores the incoming engine and rudder values in driveValues,
# and uses these values to drive the boat using driveBoat() of Control.py
def driveBoat(leftEngine, rightEngine, rudder):
	driveValues = [leftEngine, rightEngine, rudder]
	c.driveBoat(leftEngine, rightEngine, rudder)

# Old states of controllable, followQuay and followCoords
oldControllable = oldFollowQuay = oldFollowCoords = False

print('Running boat Controller')
# Initalize controller with arduino.
c = Controller()
# Initialize class handlers.
quayHandle = QuayHandle(c)
coordsHandle = CoordsHandle(c)
# Set old controllable state
oldControllable = c.controllable
print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'followCoords': coordsHandle.instance.running}))

# Flush stdout before we start.
sys.stdout.flush()
while True:
	# Wait for input from NodeJS
	userinput = sys.stdin.readline()
	if(not c.connected):
		c = Controller()
		print(json.dumps({'controllable': c.controllable}))
		sleep(0.5)
		sys.stdout.flush()
		continue
	
	# If the length is more than 1, NodeJS Pushes an empty string time to time and also one character time to time.
	if(len(userinput) > 1):
		# Parse to python json object (list)
		jsonObj = json.loads(userinput)

		# Set currentLocation of followCoords
		if 'currentLocation' in jsonObj:
			coordsHandle.instance.setPosition(jsonObj['currentLocation'])

		# Put values in correct variables
		if 'temperature'  in jsonObj:
			temperature = jsonObj['temperature']

			# Temperature will be given on initialization of the connection.
			if not quayHandle.instance.running:
				# Update Quay follower instance
				quayHandle.setTemperature(temperature)
			sys.stdout.flush()
			continue
	
		# If controllable send data to arduino.
		if c.controllable:
			# Start following the quay wall
			if 'followQuay' in jsonObj and not coordsHandle.followCoords:
				quayHandle.updateQuayFollow(jsonObj['followQuay'], 15)
			
			# Start following coordinates
			if 'followCoords' in jsonObj and not quayHandle.followQuay:
				coordsHandle.updateCoordsFollow(jsonObj['followCoords'], 50, jsonObj['goalLocation'])
			
			# Print the states and engine,rudder,sensor values if followQuay is running
			if quayHandle.instance.running:
				print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'sensorDistances' : quayHandle.instance.pings, 'followCoords': coordsHandle.instance.running, 'driveValues': driveValues}))
				sys.stdout.flush()
				continue
			
			# Print states and engine and rudder values
			if coordsHandle.instance.running:
				print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'followCoords': coordsHandle.instance.running, 'driveValues': driveValues }))
				sys.stdout.flush()
				continue

			
			# Trying to write data to arduino.
			# If the engines and rudder is set.
			if 'leftEngine' in jsonObj and 'rightEngine' in jsonObj and 'rudder' in jsonObj:
				c.driveBoat(jsonObj['leftEngine'], jsonObj['rightEngine'], jsonObj['rudder'])
		else:
			print('Uncontrollable!')
			# Checks if still uncontrollable.
			c.check()
			# Stop the follow quay wall thread if boat is not controllable
			if quayHandle.instance.running:
				quayHandle.updateQuayFollow(False, 0)
				print('Quay is stopping')
			# Stop the follow coords wall thread if boat is not controllable
			if coordsHandle.instance.running:
				coordsHandle.updateCoordsFollow(False,0,[])
				print('Coords is stopping')

	# Only print if the new state is different than the old state.			
	if c.controllable is not oldControllable or quayHandle.instance.running is not oldFollowQuay or coordsHandle.instance.running is not oldFollowCoords:
		oldControllable = c.controllable
		oldFollowQuay = quayHandle.instance.running
		oldFollowCoords = coordsHandle.instance.running
		print(json.dumps({'controllable': c.controllable, 'followQuay': quayHandle.instance.running, 'followCoords': coordsHandle.instance.running}))
	# Flush because of the while loop it wont print otherwise.
	sys.stdout.flush()
