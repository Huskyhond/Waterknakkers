#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Current12 Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_current12 import BrickletCurrent12

# Callback function for current callback (parameter has unit mA)
def cb_current(current):
    print("Current: " + str(current/1000.0) + " A")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    c = BrickletCurrent12(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register current callback to function cb_current
    c.register_callback(c.CALLBACK_CURRENT, cb_current)

    # Set period for current callback to 1s (1000ms)
    # Note: The current callback is only called every second
    #       if the current has changed since the last call!
    c.set_current_callback_period(1000)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
