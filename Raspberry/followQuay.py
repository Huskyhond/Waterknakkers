#from ultraSonic import Ping
#from Control import *
import math
import numpy as np
import threading as th
from time import sleep

class Follow:
    def __init__(self, max_motorPower, sensorAngle = 45, debug = False):
        self.debug = debug
        self.sensorAngle = sensorAngle
        self.max_motorPower = max_motorPower/100
        self.t = None
        self.running = False
        self.test = False


    def calcBoatAngle(self, sensorDistances):
        correctDistance = sensorDistances[0] / math.cos(self.sensorAngle)
        errorDistance = sensorDistances[1] - correctDistance
        perpendicular = math.sqrt(math.pow(correctDistance,2) - math.pow(sensorDistances[0],2))
        wallLength = math.sqrt(math.pow(errorDistance,2) + math.pow(perpendicular,2) -2 * errorDistance * perpendicular * math.cos(math.radians(180-self.sensorAngle)))
        a = errorDistance * math.sin(math.radians(180-self.sensorAngle))
        angle = math.degrees(math.asin(a/wallLength))
        return angle

    #change incoming value in set range to value in other given range
    def map(self, x, in_min, in_max, out_min, out_max):
        return np.clip(int(((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)*100 )/100,out_min,out_max)

    def adjustBoat(self):
        # Calculate the angle of the boat using the ultrasonic sensors
        boatAngle = self.calcBoatAngle([2,9.9]) 
        motorL = motorR = self.max_motorPower
        
        if boatAngle < 0: # Steer boat to right
            if self.debug: print("Steer Right")
            # Adjust motorR speed in range from 0 to the max_self.max_motorPower
            motorR = self.map(boatAngle, -90, 90, 0, self.max_motorPower)*2

        else: # Steer boat to left
            if self.debug: print("Steer Left")
            # Adjust motorL speed in range from 0 to the max_self.max_motorPower
            motorL = (self.max_motorPower*2)-self.map(boatAngle, -90, 90, 0, self.max_motorPower)*2

        # Adjust rudder angle to the boat angle
        rudder = self.map(boatAngle, -50, 50, -1, 1)*-1

        #motorR = 100 + ((boatAngle / 90) * 100)
        #motorL = (1 - (boatAngle / 90)) * 100
        #motorL = round(self.max_motorPower * (motorL/100))
        #motorR = round(self.max_motorPower * (motorR/100))

        if self.debug:
            print("Boat angle:", boatAngle)    
            print("MotorL:", motorL)
            print("MotorR:", motorR)
            print("Rudder:", rudder)

        return [motorL,motorR,rudder]

    def follow(self):
        while self.running:
            self.adjustBoat()

    def start(self):
        if self.t is None and not self.running:
            self.t = th.Thread(target=self.follow)
            self.t.daemon = True
            self.running = True
            self.t.start()
            print("Follow start")
        else:
            print("Already running")


    def stop(self):
        if self.t and self.running:
            self.running = False
            self.t.join()
            self.t = None
            print("Follow stop")
        else:
            print("Not running")

f = Follow(50, debug = True)
f.start()
sleep(2)
f.stop()



