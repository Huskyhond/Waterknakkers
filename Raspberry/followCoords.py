#--------------------------------
#Boris van Norren
#Hogeschool Rotterdam
#0835560
#TI3A
#Waterknakkers
#--------------------------------
from IMU import *
import threading as th
from time import sleep
import numpy as np
import math
import os

class Coords():
    def __init__(self, callback, max_power, goal, debug = False):
        self.imu = IMU()
        self.imu.connect()
        self.coordinates = [0,0]
        self.goal = goal[1]
        self.goalNumber = 1
        self.max_power = max_power/100
        self.debug = debug
        self.t = None
        self.running = False 
        self.cb = callback
        self.goalAngle = None
        self.boatAngle = None

    def setPosition(self, coordinates):
        self.coordinates = coordinates                

    def setGoal(self, newGoal):
        self.goal = newGoal

    def setCoord(self, coord, number):
        self.goal[number] = coord

    # Change human readable values to values used by the boat.
    def map(self, x, in_min, in_max, out_min, out_max):
        return np.clip(int(((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)*100 )/100,out_min,out_max)

    # Calculate boatangle from starting point 
    def calcGoalAngle(self):
        dLng = self.goal[0] - self.coordinates[0]
        dLat = self.goal[1] - self.coordinates[1]
        
        East = 0 if dLng < 0 else 1
        North = 0 if dLat < 0 else 1
        
        if(North == 1 & East == 1):
            print("test1")
            goalAngle = math.degrees(math.atan(dLng / dLat))
        elif(North == 0 & East == 1):
            goalAngle = math.degrees(math.atan(dLat / dLng)) + 90
        elif(North == 0 & East == 0):
            goalAngle = math.degrees(math.atan(dLng / dLat)) + 180
        elif(North == 1 & East == 0):
            goalAngle = math.degrees(math.atan(dLat / dLng)) + 270
        return goalAngle

    def rotateBoat(self):
        os.system('cls')
        self.boatAngle = self.imu.get_orientation()
        motorL = motorR = rudder = 0
        if(self.goalAngle is None):
            self.goalAngle = self.calcGoalAngle()

        #self.goalAngle = 190
        #self.boatAngle = 350
        clock = True

        if self.goalAngle > 180:
            turningPoint = self.goalAngle - 180
            if self.boatAngle > self.goalAngle or self.boatAngle < turningPoint:
                clock = False
        else:
            turningPoint = self.goalAngle + 180
            if self.boatAngle > self.goalAngle and self.boatAngle < turningPoint:
                clock = False
            
        if clock:
            # Turn counter clockwise
            if(self.debug): print("Turn counter-clockwise")
            motorR = 1
            motorL = -1
            rudder = -1
        else:
            # Turn clockwise
            if(self.debug): print("Turn clockwise")
            motorR = -1
            motorL = 1
            rudder = 1

        marge = abs(self.goalAngle - self.boatAngle) if abs(self.goalAngle - self.boatAngle) < 180 else 360 - abs(self.goalAngle - self.boatAngle)       
        

        if(self.debug):
            print("-----Turning boat----")
            print("TurningPoint:",turningPoint)
            print("Goal Angle: ", self.goalAngle)
            print("Boat angle:", self.boatAngle) 
            print("MotorL:", motorL)
            print("MotorR:", motorR)
            print("Rudder: ", rudder)
            print("Marge:", marge)
        return [marge, motorL, motorR, rudder]

    def sailBoat(self, marge):
        # self.boatAngle = calcDeltaBoatAngle()
        motorL = motorR = self.max_power
        rudder = 0
        
        marge = abs(self.goalAngle - self.boatAngle) if abs(self.goalAngle - self.boatAngle) < 180 else 360 - abs(self.goalAngle - self.boatAngle)       

        if(self.debug):
            print("-----Sailing boat----")
            print("Goal Angle: ", self.goalAngle)
            print("Boat angle:", self.boatAngle) 
            print("MotorL:", motorL)
            print("MotorR:", motorR)
            print("Rudder: ", rudder)
            print("Marge:", marge)
        return [marge, motorL, motorR, rudder]

    def checkGoal(self):
        pass

    def run(self):
        # Keep adjusting the boat using the callback until running is set to false
        while self.running:
            print('while')
            if self.cb is not None:
                rotateValues = self.rotateBoat()
                driveValues = rotateValues
                marge = rotateValues[0]
                if(marge < 20):
                    speedValues = self.sailBoat(marge)
                    driveValues = speedValues
                sleep(1)
                self.cb(driveValues[1], driveValues[2], driveValues[3])
            else:
                print('cb is none')
        print('running:', self.running)

    def start(self):
        if self.t is None and not self.running:
            self.t = th.Thread(target=self.run)
            self.t.daemon = True
            self.running = True
            self.t.start()
            if(self.debug): print("followCoords start")
        else:
            if(self.debug): print("followCoords already running")


    def stop(self):
        if self.t and self.running:
            self.running = False
            self.t.join()
            self.t = None
            if(self.debug): print("followCoords stop")
        else:
            if(self.debug): print("followCoords not running")

# START_COORD = [51.89883324259825, 4.4081997871398935]
# GOAL = [51.8983036195826, 4.405646324157716]

START_COORD = [53, 5]
GOAL = [[55, 6], [55,4], [51,4], [51,6]]

def foo(x,y,z):
    print(x,y,z)

c = Coords(foo, 45, GOAL, True)
c.setPosition(START_COORD)
c.start()
while True:
    pass