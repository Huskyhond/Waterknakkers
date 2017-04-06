#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Industrial Dual Analog In Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_dual_analog_in import BrickletIndustrialDualAnalogIn

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    idai = BrickletIndustrialDualAnalogIn(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get current voltage from channel 1 (unit is mV)
    voltage = idai.get_voltage(1)
    print("Voltage (Channel 1): " + str(voltage/1000.0) + " V")

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
