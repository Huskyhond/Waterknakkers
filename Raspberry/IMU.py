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
        
    def connect(self):
        # Connect the IP connection to the IMU brick
        self.ipcon.connect(self.HOST, self.PORT)
        # Refresh the timer of the Callback to REFRESH_TIME
        self.imu.set_all_data_period(self.REFRESH_TIME)

    def disconnect(self):
        self.ipcon.disconnect()
