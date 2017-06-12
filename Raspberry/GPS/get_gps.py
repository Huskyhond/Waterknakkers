#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "suA" # Change XYZ to the UID of your GPS Bricklet
import sys
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps import BrickletGPS

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    gps = BrickletGPS(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    while(True):
    # Get current coordinates
      userinput = sys.stdin.readline()
      latitude, ns, longitude, ew, pdop, hdop, vdop, epe = gps.get_coordinates()

      print("[" + str(latitude/1000000.0) + "," + str(longitude/1000000.0) + "]")
      sys.stdout.flush()
