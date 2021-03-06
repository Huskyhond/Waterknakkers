import platform
# Only import and use ultrasonic sensors if system uses Linux.
# This enables the script to be run on a Windows machine.
isLinux = False
if "Linux" in platform.system():
    from ultraSonic import Ping
    isLinux = True
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
            self.p = Ping(temperature)              # The Ping class to get ping sensor measurement
            print("Ping sensors initialized!")
        else: 
            self.p = None
            print("Ping sensors not initialized. OS is not Linux")
        self.pings = [4,5.66,500]                   # The ping sensor measurement values
        self.whichAdjustBoatToUse = 1               # Which adjustBoat function to use

    # Calculate the relative angle from the boat to the wall
    def calcAngle(self, sensorDistances):
        x = sensorDistances[0]          # The distance from the boat to the Quay wall
        y = sensorDistances[1]          # The distance from the boat to the Quay wall with an 45 degrees angle
        sensorAngle = self.sensorAngle  # The angle between the 2 sensors facing the Quay wall
        
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

    # Change incoming value in set range to value in other given range
    # And clip the output value between the out_min and out_max interval
    def map(self, x, in_min, in_max, out_min, out_max):
        x, in_min, in_max, out_min, out_max = float(x), float(in_min), float(in_max), float(out_min), float(out_max)
        res = np.clip( ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min) , out_min, out_max)
        return float(res)

    # Get sensor data is possible
    def getPings(self):
        # Set pings values to the ping sensors measurements
        if isLinux: self.pings = [self.p.measure(2),self.p.measure(1),self.p.measure(0)]
        # If the OS is not linux(raspberry pi), then return default values
        else: self.pings = [4,5.66,500]

    # Adjust boat using 2 sensors with perpendicular and 45 degrees
    def adjustBoat(self):
        self.getPings()
        # Calculate the angle of the boat using the ultrasonic sensors
        boatAngle = self.calcAngle(self.pings) 
        # Set the default motor power to max_motorPower
        motorL = motorR = self.max_motorPower

        # Steer boat to right when front wall in sight
        if self.pings[2] < 150:
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


    # Adjust boat using only 1 sensor
    def adjustBoat2(self):
        quayWallDistance = self.p.measure(2)
        frontWallDistance = self.p.measure(0)

        # Idle motors if sensors timeout
        if quayWallDistance is 0 or frontWallDistance is 0:
            print("return [0]")
            return [0,0,0]

        motorL = motorR = rudder = 0.0
        power = 0.25
        setQuayDistance = 80
        deadZone = 5

        # Front wall in sight, steer right
        if frontWallDistance < 250:
            if self.debug: print("Front wall, Steer Right")
            motorL = 0.5
            motorR = -0.5
            rudder = 1

        # Steer left
        elif quayWallDistance > setQuayDistance+deadZone:
            if self.debug: print("Steer Left")
            motorL = 0.0
            motorR = power
            rudder -= (abs(setQuayDistance - quayWallDistance)*0.25)/100
            rudder = np.clip(rudder, -1,0)
        # Steer right
        elif quayWallDistance < setQuayDistance-deadZone:
            if self.debug: print("Steer Right")
            motorL = power
            motorR=  0.0
            rudder += (abs(setQuayDistance - quayWallDistance)*0.25)/100
            rudder = np.clip(rudder, 0,1)
        # Go straight if in deadzone
        else:
            motorL = motorR = power
            rudder = 0
        
        if self.debug:
            print("Sensor Distances:",[quayWallDistance,frontWallDistance])
            print("Drive:", motorL, motorR, rudder)

        return [motorL, motorR, rudder] 

    # Adjust boat using 2 sensors with both 30 degrees angle
    def adjustBoat3(self):
        quayWallDistance1 = self.p.measure(2) # First quay sensor
        quayWallDistance2 = self.p.measure(1) # Second quay sensor
        frontWallDistance = self.p.measure(0) # Front sensor

        # Idle motors if sensors timeout
        if quayWallDistance1 is 0 or quayWallDistance2 is 0 or frontWallDistance is 0:
            return [0,0,0]

        motorL = motorR = rudder = 0.0
        power = 0.5
        setQuayDistance = 100
        deadZone = 30

        # Front wall in sight, steer right
        if frontWallDistance < 200:
            if self.debug: print("Front wall, Steer Right")
            motorL = power
            motorR = -power
            rudder = 1.0
        # Sensors in deadzone
        elif abs(quayWallDistance2 - quayWallDistance1) <= deadZone:
            if self.debug: print("In deadzone, Go Straight")
            motorL = motorR = power
            rudder = 0
        # Steer left
        elif quayWallDistance1 <= quayWallDistance2:
            if self.debug: print("Steer Left")
            motorL = 0.0
            motorR = power
            rudder = -0.8
        # Steer right
        elif quayWallDistance2 < quayWallDistance1:
            if self.debug: print("Steer Right")
            motorL = power
            motorR= 0.0
            rudder = 0.8

        if self.debug:
            print("Sensor Distances:", [quayWallDistance, frontWallDistance], "Drive:", motorL, motorR, rudder)

        return [motorL, motorR, rudder] 

    # The thread target function
    def follow(self):
        # Keep adjusting the boat using the callback until running is set to false
        while self.running:
            if self.cb is not None:
                if self.whichAdjustBoatToUse is 0: driveValues = self.adjustBoat()
                elif self.whichAdjustBoatToUse is 1: driveValues = self.adjustBoat2()
                elif self.whichAdjustBoatToUse is 2: driveValues = self.adjustBoat3()
                self.cb(driveValues[0], driveValues[1], driveValues[2])
                sleep(0.3)

    # Start thread if possible
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

    # Stop thread if possible
    def stop(self):
        # Stop follow quay thread
        if self.t and self.running:
            self.running = False
            self.t.join()
            self.t = None
            print("Follow stop")
        else:
            print("Follow not running")




# Test callback
def foo(x,y,z):
    pass

# Test function to test the followQuay for 400s
def test():
    f = Follow(foo, 100, debug = True)
    f.start()
    sleep(400)
    f.stop()

#test()


