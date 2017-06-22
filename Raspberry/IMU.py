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
    """
    The IMU Brick by TinkerForge. \n
    This unit will automatically configure itself to the IMU located in boat Anna.
    """
    def __init__(self, debug = False):
        self.HOST = "localhost"
        self.PORT = 4223
        self.UID = "62Bous"
        self.REFRESH_TIME = 50
        self.debug = debug
        self.ipcon = IPConnection()
        self.imu = BrickIMUV2(self.UID, self.ipcon)

    def get_all_data(self):
        """
        This will return all data collected by the IMU
        """
        data = self.imu.get_all_data()
        return data
        
    def connect(self):
        """
        Calling this function will connect the client with the IMU brick.
        """
        try:
            self.ipcon.connect(self.HOST, self.PORT)
        except Exception:
            print("Can't connect to the IMU brick")
            return False
        # Refresh the timer of the Callback to REFRESH_TIME
        self.imu.set_all_data_period(self.REFRESH_TIME)
        return True

    def disconnect(self):
        """
        Disconnect from IMU brick
        """
        self.ipcon.disconnect()
