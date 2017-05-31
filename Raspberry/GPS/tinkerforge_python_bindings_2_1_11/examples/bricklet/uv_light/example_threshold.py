#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your UV Light Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_uv_light import BrickletUVLight

# Callback function for UV light reached callback (parameter has unit µW/cm²)
def cb_uv_light_reached(uv_light):
    print("UV Light: " + str(uv_light) + " µW/cm²")
    print("UV Index > 3. Use sunscreen!")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    uvl = BrickletUVLight(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get threshold callbacks with a debounce time of 10 seconds (10000ms)
    uvl.set_debounce_period(10000)

    # Register UV light reached callback to function cb_uv_light_reached
    uvl.register_callback(uvl.CALLBACK_UV_LIGHT_REACHED, cb_uv_light_reached)

    # Configure threshold for UV light "greater than 750 µW/cm²" (unit is µW/cm²)
    uvl.set_uv_light_callback_threshold(">", 750, 0)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
