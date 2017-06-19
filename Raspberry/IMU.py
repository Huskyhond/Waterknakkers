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
        self.debug = debug
        self.ipcon = IPConnection()
        self.imu = BrickIMUV2(self.UID, self.ipcon)

    def get_orientation(self):
        data = self.imu.get_all_data()
        return data
        
    def connect(self):
        # Connect the IP connection to the IMU brick
        try:
            self.ipcon.connect(self.HOST, self.PORT)
        except Exception:
            print("Can't connect to the IMU brick")
            return False
        # Refresh the timer of the Callback to REFRESH_TIME
        self.imu.set_all_data_period(self.REFRESH_TIME)
        return True

    def disconnect(self):
        self.ipcon.disconnect()
