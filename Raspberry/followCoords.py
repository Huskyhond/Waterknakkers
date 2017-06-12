#--------------------------------
#Boris van Norren
#Hogeschool Rotterdam
#0835560
#TI3A
#Waterknakkers
#--------------------------------
from IMU import *
from GPS import gps_callback

class Coords():
    def __init__(self, max_power,goal):
        self.imu.connect()
        # Get the boat's coordinates
        self.coordinates = gps_callback.cb_coordinates()
        self.goal = goal
        self.max_power = max_power/100

    def setGoal(self, newGoal):
        self.goal = newGoal

    def setCoord(self, coord, number):
        goal[number] = coord

    # Change human readable values to values used by the boat.
    def map(self, x, in_min, in_max, out_min, out_max):
        return np.clip(int(((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)*100 )/100,out_min,out_max)

    # Calculate boatangle from starting point 
    def calcDeltaBoatAngle(self):
        H, R, P = self.imu.get_orientation()
        currentBoatAngle = H
        dLng = goal[0] - self.goal[0]
        dLat = goal[1] - self.goal[1]
        
        East = 0 if dLng < 0 else East = 1
        North = 0 if dLat < 0 else North = 1
        
        if(North == 1 & East == 1):
            desiredAngle = math.atan(dLat / dLng)
        if(North == 0 & East == 1):
            desiredAngle = math.atan((dLat *-1) / dLng) + 90
        if(North == 0 & East == 0):
            desiredAngle = (math.atan((dLat *-1) / (dLng * -1)) + 180) - 360
        if(North == 1 & East == 0):
            desiredAngle = (math.atan(dLat / (dLng * -1)) + 270) - 360

        return desiredAngle - currentBoatAngle


    def run(self):
        if(calcDeltaBoatAngle() > 0):
            # Turn clockwise
            motorL = motorR = self.max_power
        elif(calcDeltaBoatAngle() < 0):
            # Turn counter clockwise
            

coord = Coords()
coord.calcBoatAngle(9)