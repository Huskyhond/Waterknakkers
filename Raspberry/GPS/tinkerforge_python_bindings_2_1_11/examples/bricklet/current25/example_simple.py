#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Current25 Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_current25 import BrickletCurrent25

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    c = BrickletCurrent25(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get current current (unit is mA)
    current = c.get_current()
    print("Current: " + str(current/1000.0) + " A")

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
