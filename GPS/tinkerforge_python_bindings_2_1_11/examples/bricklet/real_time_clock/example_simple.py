#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Real-Time Clock Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_real_time_clock import BrickletRealTimeClock

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    rtc = BrickletRealTimeClock(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get current date and time
    year, month, day, hour, minute, second, centisecond, weekday = rtc.get_date_time()

    print("Year: " + str(year))
    print("Month: " + str(month))
    print("Day: " + str(day))
    print("Hour: " + str(hour))
    print("Minute: " + str(minute))
    print("Second: " + str(second))
    print("Centisecond: " + str(centisecond))
    print("Weekday: " + str(weekday))

    # Get current timestamp (unit is ms)
    timestamp = rtc.get_timestamp()
    print("Timestamp: " + str(timestamp) + " ms")

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
