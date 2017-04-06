#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Accelerometer Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_accelerometer import BrickletAccelerometer

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    a = BrickletAccelerometer(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get current acceleration (unit is g/1000)
    x, y, z = a.get_acceleration()

    print("Acceleration[X]: " + str(x/1000.0) + " g")
    print("Acceleration[Y]: " + str(y/1000.0) + " g")
    print("Acceleration[Z]: " + str(z/1000.0) + " g")

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
