import serial

class ArduinoCommunication:

    def __init__(self):
        self.serial = serial.Serial('/dev/ttyACM0', 9600) 
