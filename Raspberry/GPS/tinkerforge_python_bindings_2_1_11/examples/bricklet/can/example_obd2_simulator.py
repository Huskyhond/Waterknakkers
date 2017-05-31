#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a minimal ODB-II simulator example that reports two erasable DTCs.
# The complete ODB-II protocol is much bigger, see https://en.wikipedia.org/wiki/OBD-II_PIDs

HOST = "localhost"
PORT = 4223
UID = "333" # Change to your UID

PID_REQUEST = 0x07DF
PID_RESPONSE = 0x07E8

MIL = 1
DCT = [0b11100100, 0b01110111, 0b00000000, 0b00000001] # U2477, P0001
DCT_COUNT = 2

from tinkerforge.bricklet_can import BrickletCAN
from tinkerforge.ip_connection import IPConnection

def cb_frame_read(can, frame_type, identifier, data, length):
    if frame_type != can.FRAME_TYPE_STANDARD_DATA or identifier != PID_REQUEST:
        return

    length = data[0]
    mode = data[1]
    pid = data[2]

    global MIL
    global DCT
    global DCT_COUNT

    if mode == 1:
        if pid == 0x00:
            print("Reporting supported mode 1 PIDs: 0x01")
            data = (PID_RESPONSE, [6, mode + 64, pid, 1 << 7, 0, 0, 0, 0x99], 8)
            can.write_frame(can.FRAME_TYPE_STANDARD_DATA, *data)
        elif pid == 0x01:
            print("Reporting monitor status")
            data = (PID_RESPONSE, [6, mode + 64, pid, (MIL << 7) | DCT_COUNT, 0, 0, 0, 0x99], 8)
            can.write_frame(can.FRAME_TYPE_STANDARD_DATA, *data)
    elif mode == 3:
        print("Reporting DTCs")
        data = (PID_RESPONSE, [6, mode + 64, DCT_COUNT] +  DCT + [0x99], 8)
        can.write_frame(can.FRAME_TYPE_STANDARD_DATA, *data)
    elif mode == 4:
        print("Clearing DCTs and turning MIL off")
        MIL = 0
        DCT = [0x99, 0x99, 0x99, 0x99]
        DCT_COUNT = 0

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    can = BrickletCAN(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register frame read callback to function cb_frame_read
    can.register_callback(can.CALLBACK_FRAME_READ, lambda *args: cb_frame_read(can, *args))

    # Enable frame read callback
    can.enable_frame_read_callback()

    # Set baud rate to 500 kbit/s
    can.set_configuration(can.BAUD_RATE_500KBPS, can.TRANSCEIVER_MODE_NORMAL, 0)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
