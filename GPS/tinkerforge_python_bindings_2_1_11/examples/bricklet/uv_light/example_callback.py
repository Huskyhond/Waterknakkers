#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your UV Light Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_uv_light import BrickletUVLight

# Callback function for UV light callback (parameter has unit µW/cm²)
def cb_uv_light(uv_light):
    print("UV Light: " + str(uv_light) + " µW/cm²")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    uvl = BrickletUVLight(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register UV light callback to function cb_uv_light
    uvl.register_callback(uvl.CALLBACK_UV_LIGHT, cb_uv_light)

    # Set period for UV light callback to 1s (1000ms)
    # Note: The UV light callback is only called every second
    #       if the UV light has changed since the last call!
    uvl.set_uv_light_callback_period(1000)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
