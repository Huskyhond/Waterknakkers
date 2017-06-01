from Control import *
import sys, json, math
from time import sleep

print('Running boat Controller')
c = Control()

def recMotorData(motorOne, motorTwo):
    c.Motor(motorOne, motorTwo)

def recRudderData(rudder):
    c.Rudder(rudder)

while True:
	userinput = sys.stdin.readline()
	if(len(userinput) > 1):
		print('Got user input: ' + userinput + '(' + str(len(userinput)) + ')')
		jsonObj = json.loads(userinput)
		engineLeft = jsonObj[0]
		engineRight = jsonObj[1]
		rudder = jsonObj[2]
		recMotorData(engineLeft, engineRight)
		recRudderData(rudder)
        userinput =None 
	sys.stdout.flush()
