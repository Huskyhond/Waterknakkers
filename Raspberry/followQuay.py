#from ultraSonic import Ping
import math

def calcBoatAngle(sensorDistances, sensorDegrees = 45):
    correctDistance = sensorDistances[0] / math.cos(sensorDegrees)
    errorDistance = sensorDistances[1] - correctDistance
    perpendicular = math.sqrt(math.pow(correctDistance,2) - math.pow(sensorDistances[0],2))
    wallLength = math.sqrt(math.pow(errorDistance,2) + math.pow(perpendicular,2) -2 * errorDistance * perpendicular * math.cos(math.radians(180-sensorDegrees)))
    a = errorDistance * math.sin(math.radians(180-sensorDegrees))
    angle = math.degrees(math.asin(a/wallLength))
    return angle


def adjustBoat(motorPower = 50):
    boatAngle = calcBoatAngle([4,5,1]) #insert ping sensor distances here
    motorL = 100
    motorR = 100
    
    if boatAngle < 0: #Steer boat to right
        print("Steer Right")
        motorR = 100 + (100 - ((1 - (boatAngle / 90)) * 100))

    else: #Steer boat to left
        print("Steer Left")
        motorL = (1 - (boatAngle / 90)) * 100

    motorL = round(motorPower * (motorL/100))
    motorR = round(motorPower * (motorR/100))
    
    print("Boat angle:",boatAngle)    
    print("MotorL:",motorL)
    print("MotorR:",motorR)

    return [motorL,motorR]
    

adjustBoat()


