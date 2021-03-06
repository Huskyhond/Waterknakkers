#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Analog Out Bricklet 2.0

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_analog_out_v2 import BrickletAnalogOutV2

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    ao = BrickletAnalogOutV2(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Set output voltage to 3.3V
    ao.set_output_voltage(3300)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
