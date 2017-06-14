import platform
isLinux = False
if "Linux" in platform.system():
    from ultraSonic import Ping
    isLinux = True
import math
import numpy as np
import threading as th
from time import sleep

class Follow:
    def __init__(self, callback, max_motorPower, sensorAngle = 45, debug = False):
        self.debug = debug                          # Boolean whether to print or not
        self.sensorAngle = sensorAngle              # Angle between sensor1 and sensor2
        self.max_motorPower = max_motorPower/100    # The max. motor power
        self.t = None                               # The thread to follow the quay wall
        self.running = False                        # Boolean to indicate the state of t 
        self.cb = callback                          # The callback that drives the boat
        if isLinux: self.p = Ping()

    def calcBoatAngle(self, sensorDistances):
        # Sensor1: the sensor perpendicular to the boat facing the quay wall
        # Sensor2: the sensor facing the quay wall with an angle of <sensorAngle>
        # Sensor3: the sensor perpendicular to the boat facing the front wall

        # The desired distance sensor2 needs to parallel the boat to the quay wall
        correctDistance = sensorDistances[0] / math.cos(self.sensorAngle)
        # The difference between the measured distance from sensor2 and the correct distance
        errorDistance = sensorDistances[1] - correctDistance
        # The perpendicular distance between sensor1 and sensor2 from the quay wall
        perpendicular = math.sqrt(math.pow(correctDistance,2) - math.pow(sensorDistances[0],2))
        # The distance between sensor1 and sensor2
        wallLength = math.sqrt(math.pow(errorDistance,2) + math.pow(perpendicular,2) -2 * errorDistance * perpendicular * math.cos(math.radians(180-self.sensorAngle)))
        # The angle between the quay wall and perpendicular and the angle of the boat
        angle = math.degrees(math.asin((errorDistance * math.sin(math.radians(180-self.sensorAngle)))/wallLength))
        
        #a = (errorDistance * math.sin(math.radians(180-self.sensorAngle)))
        return angle

    def calcAngle(self, sensorDistances):
        x = sensorDistances[0]
        y = sensorDistances[1]
        sensorAngle = self.sensorAngle
        wall = math.sqrt(math.pow(x,2) + math.pow(y,2) - 2*x*y*math.cos(math.radians(sensorAngle)))
        angle1 = math.degrees(math.asin(((y*math.sin(math.radians(sensorAngle)))/wall)))
        angle2 = math.degrees(math.asin(((x*math.sin(math.radians(sensorAngle)))/wall)))

        if x > y:
            angle3 = 180 - 45 - angle1
            return angle3
            #print(wall,angle3,angle1)
        else:
            angle3 = 180 - 45 - angle2
            return angle3
            #print(wall,angle3,angle2)

    
    def map(self, x, in_min, in_max, out_min, out_max):
        # Change incoming value in set range to value in other given range
        # Round the output on 2 decimals and clips the output value between the out_min and out_max interval
        return np.clip(int(((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)*100 )/100,out_min,out_max)

    def getPings(self):
        if isLinux: pings = [self.p.measure(2),self.p.measure(1)]
        else: pings = [4,7.62]
        if self.debug: print(pings)
        return pings

    def adjustBoat(self):
        # Calculate the angle of the boat using the ultrasonic sensors
        #boatAngle = self.calcBoatAngle([4,10]) 
        boatAngle = self.calcAngle(self.getPings()) 
        
        
        # Set the default motor power to max_motorPower
        motorL = motorR = self.max_motorPower

        # Steer boat to right
        if boatAngle < 90: 
            if self.debug: print("Steer Right")
            # Adjust motorR speed in range from 0 to the max_self.max_motorPower
            motorR = self.map(boatAngle, -90, 90, 0, self.max_motorPower)*2
        
        # Steer boat to left
        else: 
            if self.debug: print("Steer Left")
            # Adjust motorL speed in range from 0 to the max_self.max_motorPower
            motorL = (self.max_motorPower*2)-self.map(boatAngle, -90, 90, 0, self.max_motorPower)*2

        # Adjust rudder angle to counter steer the boat
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

        # Return the motor power and the rudder angle
        return [motorL,motorR,rudder]

    def follow(self):
        # Keep adjusting the boat using the callback until running is set to false
        while self.running:
            if self.cb is not None:
                driveValues = self.adjustBoat()
                self.cb(driveValues[0], driveValues[1], driveValues[2])

    def start(self):
        # Start thread to follow the quay wall
        if self.t is None and not self.running:
            self.t = th.Thread(target=self.follow)
            self.t.daemon = True
            self.running = True
            self.t.start()
            print("Follow start")
        else:
            print("Follow already running")


    def stop(self):
        # Stop follow quay thread
        if self.t and self.running:
            self.running = False
            self.t.join()
            self.t = None
            print("Follow stop")
        else:
            print("Follow not running")


def foo(x,y,z):
    pass

def test():
    f = Follow(foo, 50, sensorAngle=45, debug = True)
    f.start()
    sleep(60)
    f.stop()


test()
#angle = math.degrees(math.asin((54 * math.sin(math.radians(45)))/38))



