#from ultraSonic import Ping
import math


sensorDistances = [4,9]
sensorDegrees = 45

def calcBoatAngle():
    correctDistance = sensorDistances[0] / math.cos(sensorDegrees)
    errorDistance = sensorDistances[1] - correctDistance
    perpendicular = math.sqrt(math.pow(correctDistance,2) - math.pow(sensorDistances[0],2))
    wallLength = math.sqrt(math.pow(errorDistance,2) + math.pow(perpendicular,2) -2 * errorDistance * perpendicular * math.cos(math.radians(135)))
    a = errorDistance * math.sin(math.radians(135))
    angle = math.degrees(math.asin(a/wallLength))
    print(angle)


    

calcBoatAngle()


