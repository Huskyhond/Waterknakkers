#from ultraSonic import Ping
import math


 #Sensors perpendicular to wall, angled to wall, forward

def calcBoatAngle(sensorDistances, sensorDegrees = 45):
    correctDistance = sensorDistances[0] / math.cos(sensorDegrees)
    errorDistance = sensorDistances[1] - correctDistance
    perpendicular = math.sqrt(math.pow(correctDistance,2) - math.pow(sensorDistances[0],2))
    wallLength = math.sqrt(math.pow(errorDistance,2) + math.pow(perpendicular,2) -2 * errorDistance * perpendicular * math.cos(math.radians(180-sensorDegrees)))
    a = errorDistance * math.sin(math.radians(180-sensorDegrees))
    angle = math.degrees(math.asin(a/wallLength))
    return angle


def adjustBoat():
    boatAngle = calcBoatAngle([2,7,1])
    print(boatAngle)    
    
    if boatAngle < 0:
        print("Steer Right")
    else:
        print("Steer Left")



adjustBoat()


