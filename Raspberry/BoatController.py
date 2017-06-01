from Control import *
import sys, json, math

c = Control()

def recMotorData(motorOne, motorTwo):
    motorOne = math.min(motorOne, 1)
    motorOne = math.max(motorOne, -1)
    motorTwo = math.min(motorTwo, 1)
    motorTwo = math.max(motorTwo, -1)
    c.Motor(motorOne, motorTwo)

def recRudderData(rudder):
    rudder = math.min(rudder, 1)
    rudder = math.max(rudder, -1)
    c.Rudder(rudder)

while True:
    userinput = sys.stdin.readline()
    if(len(userinput) > 1):
        print('Got user input: ' + userinput + '(' + str(len(userinput)) + ')')
        json = json.loads(userinput)
        engineLeft = json[0]
        engineRight = json[1]
        rudder = json[2]
        recMotorData(engineLeft, engineRight)
        recRudderData(rudder)
        break