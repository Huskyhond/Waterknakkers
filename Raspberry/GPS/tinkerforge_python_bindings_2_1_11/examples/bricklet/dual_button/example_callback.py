#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "XYZ" # Change XYZ to the UID of your Dual Button Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button import BrickletDualButton

# Callback function for state changed callback
def cb_state_changed(button_l, button_r, led_l, led_r):
    if button_l == DualButton.BUTTON_STATE_PRESSED:
        print("Left button pressed")
    else:
        print("Left button released")

    if button_r == DualButton.BUTTON_STATE_PRESSED:
        print("Right button pressed")
    else:
        print("Right button released")

    print("")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    db = BrickletDualButton(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register state changed callback to function cb_state_changed
    db.register_callback(db.CALLBACK_STATE_CHANGED, cb_state_changed)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
