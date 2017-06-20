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

#Debug values
START_COORD = [53, 5]
GOAL = [[53, 5], [54, 4], [54,6], [52,4], [52,6]]

class Coords():
    """
    This class performs GPS-to-GPS navigation with the Tinkerforge IMU v2.0 \n
    :callback: Callback function that returns the driveValues of the boat \n
    :max_power: The boat's max_power. \n 
    :goal: Array of coordinates with the first input being the boat's own coordinates \n
    :debug: If debug is true, it will print most values. Default = False
    """
    def __init__(self, callback, max_power, goal, debug = False):
        self.imu = IMU()
        self.connected = self.imu.connect()
        self.goalNumber = 1
        self.totalGoal = goal
        self.goal = self.totalGoal[self.goalNumber]
        self.coordinates = self.totalGoal[0]
        self.max_power = max_power/100
        self.debug = debug
        self.t = None
        self.running = False 
        self.cb = callback
        self.goalAngle = None
        self.boatAngle = None

    def setPosition(self, coordinates):
        """
        Set the current boat's GPS location \n
        :coordinates: [LONG,LAT]
        """
        self.coordinates = coordinates                

    def setGoal(self, newGoal):
        """
        Sets the current GPS goal of the boat \n
        :newGoal: [LONG,LAT]
        """
        self.goal = newGoal

    def map(self, x, in_min, in_max, out_min, out_max):
        """
        Change a value in a range (like 50 in 0-100) to another range relative to the  given (like 0 in -1 to 1)
        """
        x *= 100
        in_min *= 100
        in_max *= 100
        out_min *= 100
        out_max *= 100
        res = np.clip( ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min) , out_min, out_max)
        return float(res)/100

    def calcGoalAngle(self):
        """    
        Calculate the Angle to boat has to rotate to in order to reach the goal. \n
        The calculation is based on a 360 circle and the goal being in range 0-360 with 0 being North
        """
        dLng = self.goal[0] - self.coordinates[0]
        dLat = self.goal[1] - self.coordinates[1]
        goalAngle = 0
        
        East = 0 if dLng < 0 else 1
        North = 0 if dLat < 0 else 1
        
        if(North == 1 & East == 1):
            goalAngle = math.degrees(math.atan(dLng / dLat))
        elif(North == 0 & East == 1):
            goalAngle = math.degrees(math.atan(dLat / dLng)) + 90
        elif(North == 0 & East == 0):
            goalAngle = math.degrees(math.atan(dLng / dLat)) + 180
        elif(North == 1 & East == 0):
            goalAngle = math.degrees(math.atan(dLat / dLng)) + 270
        return goalAngle

    # Function to rotate the boat
    def rotateBoat(self):
        """
        Rotate the boat
        """
        motorL = motorR = rudder = 0

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
            if(self.debug): print("Turn clockwise")
            motorR = -1
            motorL = 1
            rudder = 1
        else:
            if(self.debug): print("Turn counter-clockwise")
            motorR = 1
            motorL = -1
            rudder = -1

        # marge = abs(self.goalAngle - self.boatAngle) if abs(self.goalAngle - self.boatAngle) < 180 else 360 - abs(self.goalAngle - self.boatAngle)       
        

        if(self.debug):
            print("-----Turning boat----")
            print("TurningPoint:",turningPoint)
            print("Goal Angle: ", self.goalAngle)
            print("Boat angle:", self.boatAngle) 
            print("MotorL:", motorL)
            print("MotorR:", motorR)
            print("Rudder: ", rudder)
            print("GOAL: ", self.goal)
            print("Boat Coordinates: ", self.coordinates)
        return [motorL, motorR, rudder]

    def sailBoat(self, marge):
        """
        Sail the boat
        """
        motorL = motorR = self.max_power
        rudder = 0

        if(marge > 10):
            motorR = self.map(marge, 0, 20, 0, 1)
        elif(marge <= 10):
            motorL = self.map(marge, 0, 20, 0, 1)
        
        # marge = abs(self.goalAngle - self.boatAngle) if abs(self.goalAngle - self.boatAngle) < 180 else 360 - abs(self.goalAngle - self.boatAngle)

        # This code simulates the boat moving towards the next gps location.
        # if(self.debug):
        #     if(self.coordinates[0] < self.goal[0]):
        #         self.coordinates[0] = self.coordinates[0] + 0.1
        #     else:
        #         self.coordinates[0] = self.coordinates[0] - 0.1
        #     if(self.coordinates[1] < self.goal[1]):
        #         self.coordinates[1] = self.coordinates[1] + 0.1
        #     else:
        #         self.coordinates[1] = self.coordinates[1] - 0.1

        if(self.debug):
            print("Going forward")
            print("-----Piloting boat----")
            print("Goal Angle: ", self.goalAngle)
            print("Boat angle:", self.boatAngle) 
            print("MotorL:", motorL)
            print("MotorR:", motorR)
            print("Rudder: ", rudder)
            print("Max power: ", self.max_power)
            print("GOAL: ", self.goal)
            print("Boat Coordinates: ", self.coordinates)
        return [motorL, motorR, rudder]

    def calcMarge(self):
        """
        Calculate the differnce between goalAngle and the boatAngle \n
        This is needed to know when the boat has to sail and when the boat has to rotate
        """
        data = self.imu.get_all_data()
        H, R, P = data.euler_angle
        self.boatAngle = round(H/16.0, 2)
        if(self.goalAngle is None):
            self.goalAngle = self.calcGoalAngle()
        marge = abs(self.goalAngle - self.boatAngle) if abs(self.goalAngle - self.boatAngle) < 180 else 360 - abs(self.goalAngle - self.boatAngle)
        if(self.debug):
            print("Marge: ", marge)
        return marge

    def checkGoal(self, coordinates):
        """
        https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude/8674#8674
        Calculate if the boat has reached his goal GPS
        """
        Lng = self.coordinates[0]
        Lat = self.coordinates[1]
        goalLng = coordinates[0]
        goalLat = coordinates[1]
        LatInRange = False
        LngInRange = False
        
        dLng = Lng - goalLng
        dLat = Lat - goalLat

        # This is a more precise calculation to calculate if destination is reached
        # if(dLng < 0.00001 or dLng > -0.00001):
        #     LngInRange = True
        # if(dLat < 0.00001 or dLat > -0.00001):
        #     LatInRange = True

        if(dLng < 0.0001 and dLng > -0.0001):
            LngInRange = True
        if(dLat < 0.0001 and dLat > -0.0001):
            LatInRange = True

        if(LatInRange and LngInRange):
            return True
        else:
            return False

    def run(self):
        """
        Thread.run \n
        This will run until the thread has been stopped
        """
        # Keep adjusting the boat using the callback until running is set to false
        while self.running:
            if self.cb is not None:
                if(self.connected):
                    if(self.debug):
                        os.system('cls')
                    marge = self.calcMarge()
                    if(marge < 20):
                        speedValues = self.sailBoat(marge)
                        driveValues = speedValues
                    else:
                        rotateValues = self.rotateBoat()
                        driveValues = rotateValues
                    if(self.checkGoal(self.goal)):
                        driveValues = [0,0,0]
                        self.goalNumber = self.goalNumber + 1
                        if(self.goalNumber <= len(self.totalGoal)):
                            self.setGoal(self.totalGoal[self.goalNumber])
                            self.goalAngle = self.calcGoalAngle()
                        elif(self.running):
                            if(self.debug):
                                print("Destination reached")
                            self.cb(0,0,0)
                    sleep(0.3)
                    self.cb(driveValues[0], driveValues[1], driveValues[2])
                else:
                    self.cb(0,0,0)
            else:
                print('cb is none')
        print('running:', self.running)

    def start(self):
        """
        Thread.start \n
        This will start the thread
        """
        if self.t is None and not self.running:
            self.t = th.Thread(target=self.run)
            self.t.daemon = True
            self.running = True
            self.t.start()
            if(self.debug): print("followCoords start")
        else:
            if(self.debug): print("followCoords already running")


    def stop(self):
        """
        Thread.stop \n
        This will stop the thread
        """
        if self.t and self.running:
            self.running = False
            self.t.join()
            # self.t = None
            if(self.debug): print("followCoords stop")
        else:
            if(self.debug): print("followCoords not running")

def foo(x,y,z):
    """
    Testcallback
    """
    pass

def test():
    """
    Debug tester
    """
    c = Coords(foo, 50, GOAL, debug = True)
    c.setPosition(START_COORD)
    c.start()
    while c.running:
        pass

# test()