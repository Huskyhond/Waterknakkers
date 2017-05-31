#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Humidity Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity import BrickletHumidity

# Callback function for humidity reached callback (parameter has unit %RH/10)
def cb_humidity_reached(humidity):
    print("Humidity: " + str(humidity/10.0) + " %RH")
    print("Recommended humiditiy for human comfort is 30 to 60 %RH.")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    h = BrickletHumidity(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get threshold callbacks with a debounce time of 10 seconds (10000ms)
    h.set_debounce_period(10000)

    # Register humidity reached callback to function cb_humidity_reached
    h.register_callback(h.CALLBACK_HUMIDITY_REACHED, cb_humidity_reached)

    # Configure threshold for humidity "outside of 30 to 60 %RH" (unit is %RH/10)
    h.set_humidity_callback_threshold("o", 30*10, 60*10)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
