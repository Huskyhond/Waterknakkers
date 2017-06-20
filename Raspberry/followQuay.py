import platform
isLinux = False
if "Linux" in platform.system():
    from ultraSonic import Ping
    isLinux = True
    print(platform.system())
import math
import numpy as np
import threading as th
from time import sleep

class Follow:
    def __init__(self, callback, max_motorPower, sensorAngle = 45, temperature = 20, debug = False):
        self.debug = debug                          # Boolean whether to print or not
        self.sensorAngle = sensorAngle              # Angle between sensor1 and sensor2
        self.max_motorPower = max_motorPower/100    # The max. motor power
        self.t = None                               # The thread to follow the quay wall
        self.running = False                        # Boolean to indicate the state of t 
        self.cb = callback                          # The callback that drives the boat
        if isLinux: 
            self.p = Ping(temperature)      # The Ping class to get ping sensor measurement
            print("Ping sensors initialized!")
        else: print("Ping sensors not initialized. OS is not Linux")
        self.pings = [4,5.66,200]                   # The ping sensor measurement values

    def calcAngle(self, sensorDistances):
        x = sensorDistances[0] # The distance from the boat to the Quay wall
        y = sensorDistances[1] # The distance from the boat to the Quay wall with an 45 degrees angle
        sensorAngle = self.sensorAngle # The angle between the 2 sensors facing the Quay wall
        # Calculate angle between x and the wall
        wall = math.sqrt(math.pow(x,2) + math.pow(y,2) - 2*x*y*math.cos(math.radians(sensorAngle)))
        if x > y:
            angle1 = math.degrees(math.asin(((y*math.sin(math.radians(sensorAngle)))/wall)))
            angle3 = 180 - self.sensorAngle - angle1
            return angle3
        else:
            angle2 = math.degrees(math.asin(((x*math.sin(math.radians(sensorAngle)))/wall)))
            angle3 = 180 - self.sensorAngle - angle2
            return angle3

    def map(self, x, in_min, in_max, out_min, out_max):
        # Change incoming value in set range to value in other given range
        # Clip the output value between the out_min and out_max interval
        x, in_min, in_max, out_min, out_max = float(x), float(in_min), float(in_max), float(out_min), float(out_max)
        res = np.clip( ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min) , out_min, out_max)
        return float(res)

    def getPings(self):
        # Set pings values to the ping sensors measurements
        if isLinux: self.pings = [self.p.measure(2),self.p.measure(1),self.p.measure(0)]
        # If the OS is not linux(raspberry pi), then return default values
        else: self.pings = [4,5.66,200]

    def adjustBoat2(self, setQuayDistance):
        self.getPings()
        quayWallDistance = self.pings[0]
        frontWallDistance = self.pings[2]
        motorL = motorR = rudder = 0

        # Front wall in sight, steer right
        if frontWallDistance < 250:
            if self.debug: print("Front wall, Steer Right")
            motorL = 0.15
            motorR = -0.15
            rudder = 1

        # Steer left
        if quayWallDistance > setQuayDistance:
            if self.debug: print("Steer Left")
            motorL = 0.05
            motorR = 0.15
            rudder = -1
        # Steer right
        else:
            if self.debug: print("Steer Right")
            motorL = 0.15
            motorR= 0.05
            rudder = 1

        if self.debug:
            print("Sensor Distances:",[quayWallDistance,frontWallDistance])
            print("MotorL:", motorL, "MotorR:", motorR, "Rudder:", rudder)

        return [motorL, motorR, rudder] 


    def adjustBoat(self):
        self.getPings()
        # Calculate the angle of the boat using the ultrasonic sensors
        boatAngle = self.calcAngle(self.pings) 
        # Set the default motor power to max_motorPower
        motorL = motorR = self.max_motorPower

        # Steer boat to right when front wall in sight
        if self.pings[2] < 200:
            if self.debug: print("Front wall in sight, Steer Right")
            motorL = 1 * self.max_motorPower
            motorR = -1 * self.max_motorPower
            # Adjust rudder angle to counter steer the boat
            rudder = 1

        # Steer boat to right
        elif boatAngle < 90 : 
            if self.debug: print("Steer Right")
            # Adjust motorR speed in range from 0 to the max_self.max_motorPower
            motorR = self.map(boatAngle, 60, 90, 0, 1)
            # Adjust rudder angle to counter steer the boat
            rudder = self.map(boatAngle, 65, 115, -1, 1)*-1
        
        # Steer boat to left
        else: 
            if self.debug: print("Steer Left")
            # Adjust motorL speed in range from 0 to the max_self.max_motorPower
            motorL = self.map(boatAngle, 90, 120, 0, 1)
            # Adjust rudder angle to counter steer the boat
            rudder = self.map(boatAngle, 65, 115, -1, 1)*-1

        if self.debug:
            print("Pings:", self.pings)
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
                driveValues = self.adjustBoat2(100)
                self.cb(driveValues[0], driveValues[1], driveValues[2])


    def start(self):
        # Start thread to follow the quay wall
        if self.t is None and not self.running:
            self.running = True
            self.t = th.Thread(target=self.follow)
            self.t.daemon = True
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
    f = Follow(foo, 100, debug = True)
    f.start()
    sleep(60)
    f.stop()


#test()


