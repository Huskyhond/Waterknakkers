#--------------------------------
#Boris van Norren
#Hogeschool Rotterdam
#0835560
#TI3A
#Waterknakkers
#--------------------------------

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2
from time import time
import os

class IMU:
    def __init__(self, debug = False):
        self.HOST = "localhost"
        self.PORT = 4223
        self.UID = "62Bous"
        self.REFRESH_TIME = 50
        self.prevTime = int(round(time() * 1000))
        self.debug = debug
        # List with accelerations
        self.currentTotal = []
        # DeltaTime
        self.currentdt = 0
        # Cycle counter
        self.i = 0
        # Velocity
        self.cvelocity = 0
        self.ipcon = IPConnection()
        self.imu = BrickIMUV2(self.UID, self.ipcon)

    def get_orientation(self):
        data = self.imu.get_all_data()
        H, R, P = data.euler_angle
        return round(H/16.0, 2)

    # Callback function for all data callback including linear_acceleration
    def cb_all_data(self, acceleration, magnetic_field, angular_velocity,
                    euler_angle, quaternion, linear_acceleration,
                    gravity_vector, temperature, calibration_status):
                
        # global prevTime, i, currentTotal, currentdt, cvelocity

        # Calculate Deltatime and reset
        currentTime = int(round(time() * 1000))
        deltaTime = (currentTime - prevTime)
        self.prevTime = currentTime

        a = linear_acceleration[1]/100
        dt = deltaTime/1000
        v = a/dt

        if i is 4:      
            # current velocity of UMI
            cvelocity = sum(self.currentTotal) * self.currentdt
            # current speed of UMI
            totalspeed += sum([x * (currentdt/i) for x in currentTotal])

            if(debug):
                print("Summation a:", sum([x * (currentdt/i) for x in currentTotal]))
                print("a & avg(a):", currentTotal, sum(currentTotal)/len(currentTotal))
                print("dt:" ,self.currentdt,'s')
                print("current v:", csnelheid)
                print("cvelocity:", cvelocity)

            currentTotal = []
            self.currentdt = 0
            i = 0
            if(self.speed > csnelheid):
                print("Returned speed : " + str(speed - csnelheid))
                # return speed - csnelheid
            elif(self.speed < csnelheid):
                print("Returned speed: " + str(csnelheid - speed))
                # return csnelheid - speed
        
        # To counter small errors made by the sensor, I truncate everything to 1 decimal.
        aa = float("%.1f" % (int(a*100)/float(100)))

        # To counter small errors made by the sensor, I throw everything away that is near 0.
        self.currentTotal.append(0 if aa > - 0.15 and aa < 0.15 else aa)
        currentdt += dt
        i += 1

    def connect(self):
        # Create IP Connection required for the IMU to connect.
        # Create an object to use the required functions
        # Connect the IP connection to the IMU brick
        self.ipcon.connect(self.HOST, self.PORT)
        # Create callback that returns the acceleration of the IMU Brick
        # imu.register_callback(imu.CALLBACK_ALL_DATA, cb_all_data(self.speed))
        # Refresh the timer of the Callback to REFRESH_TIME
        self.imu.set_all_data_period(self.REFRESH_TIME)
        # input("Press key to exit\n")
        # ipcon.disconnect()

    def disconnect(self):
        self.ipcon.disconnect()
