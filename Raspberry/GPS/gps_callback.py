#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "suA" # Change XYZ to the UID of your GPS Bricklet
REFRESH_TIME = 2000

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps import BrickletGPS

def file_len(fileName):
    i = None
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
    if i is None:
        return 0
    return i + 1

def line_pre(fileName, line, max_lines = 10):
    file_length = file_len(fileName)
    with open(fileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
# Callback function for coordinates callback
def cb_coordinates(latitude, ns, longitude, ew, pdop, hdop, vdop, epe):
    latStr = str(latitude/1000000.0)
    lngStr = str(longitude/1000000.0)
    
    print(latStr + "," + lngStr)

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    gps = BrickletGPS(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register coordinates callback to function cb_coordinates
    gps.register_callback(gps.CALLBACK_COORDINATES, cb_coordinates)

    # Set period for coordinates callback to 1s (1000ms)
    # Note: The coordinates callback is only called every second
    #       if the coordinates has changed since the last call!
    gps.set_coordinates_callback_period(REFRESH_TIME)

#    input("Press key to exit\n") # Use input() in Python 3
#    ipcon.disconnect()