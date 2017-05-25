#--------------------------------
#Boris van Norren
#0835560
#Waterknakkers
#--------------------------------

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2
from time import time
import os

HOST = "localhost"
PORT = 4223
UID = "62Bous"
REFRESH_TIME = 50
prevTime = int(round(time() * 1000))
# List with acc
currentTotal = []
# DeltaTime
currentdt = 0
# Cycle counter
i = 0
# Velocity
cvelocity = 0

def cb_acceleration(x, y , z):
    return x,y,z

def cb_calibrate_speed(x,y,z):
    # Example to go a constant 10km/u
    print(y/100)
    if((y/100.0) > 1):
        print("Slowdown Y")
    elif((y/100) < -1):
        print("Slowdown Y")
    else:
        print("SpeedUP Y")

# Callback function for all data callback
def cb_all_data(acceleration, magnetic_field, angular_velocity,
                euler_angle, quaternion, linear_acceleration,
                gravity_vector, temperature, calibration_status):
    
    global prevTime, i, currentTotal, currentdt, cvelocity
    
    # Calculate Deltatime and reset
    currentTime = int(round(time() * 1000))
    deltaTime = (currentTime - prevTime)
    prevTime = currentTime

    a=linear_acceleration[1]/100
    dt= deltaTime/1000
    v=a/dt
    
    if i is 4:
        os.system('cls')
        
        # current velocity of UMI
        cvelocity = sum(currentTotal) * currentdt
        # current speed of UMI
        totalspeed += sum([x * (currentdt/i) for x in currentTotal])

        print("Summation a:", sum([x * (currentdt/i) for x in currentTotal]))
        print("a & avg(a):", currentTotal, sum(currentTotal)/len(currentTotal))
        print("dt:" ,currentdt,'s')
        print("current v:", csnelheid)
        print("cvelocity:", cvelocity)

        currentTotal = []
        currentdt = 0
        i = 0
    
    aa = float("%.1f" % (int(a*100)/float(100)))
    
    currentTotal.append(0 if aa > - 0.15 and aa < 0.15 else aa)
    currentdt += dt
    i += 1

def cb_speed():
    # Create IP Connection required for the IMU to connect.
    ipcon = IPConnection()
    # Create an object to use the required functions
    imu = BrickIMUV2(UID, ipcon)
    # Connect the IP connection to the IMU brick
    ipcon.connect(HOST, PORT)
    # Create callback that returns the acceleration of the IMU Brick
    imu.register_callback(imu.CALLBACK_ALL_DATA, cb_all_data)
    # Refresh the timer of the Callback to REFRESH_TIME
    imu.set_all_data_period(REFRESH_TIME)
    input("Press key to exit\n")
    ipcon.disconnect()

cb_speed()
