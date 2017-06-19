import serial
from time import sleep
import numpy as np
from pyparsing import*

class Controller:
    def __init__(self, port='/dev/ttyACM0',baudrate=115200):
        self.debug = False
        try:
            self.ser=serial.Serial(port,baudrate)
            print('Serial port opened at:',port, 'baudrate:', baudrate)
            print("Warm-up...")
            sleep(3)
            print("Serial port Ready!")
            print(self.ser.read(self.ser.inWaiting()))
            self.connected = True   
            self.check()
        except:
            print('Opening Serial port failed, try again or try another port.')
            self.connected = False
            self.controllable = False
            
        print('Connected:',self.connected)
        self.motorL=90
        self.motorR=90
        self.rudderL=90
        self.rudderR=90

    def write(self):
        """
            Write values to arduino
            LR,RR,LM,RM
        """
        #constructs a string to send to the arduino
        writeValues = 'a'+str(int(self.rudderL))+'b'+str(int(self.rudderR))+'c'+str(int(self.motorL))+'d'+str(int(self.motorR))+'z'
        
        #send string to arduino
        if self.debug: print('write:',writeValues)
        self.ser.write(str.encode(writeValues))

        #wait 10 ms
        sleep(0.01)

        # Read echo from the arduino
        echo=self.ser.read(self.ser.inWaiting())
        if self.debug: print('echo:',echo)

        try:
            # Check if echo equals the writeValues
            if str.encode(writeValues) in echo:
                if self.debug: print('Correct echo received')
                return True
            else:
                #no data received from arduino, or incorrect format
                if self.debug: print('Incorrect or empty echo from arduino received')
                self.controllable = False
                return False
        except:
            if self.debug: print('Error comparing writeValues and echo.', 'writeValues:',str.encode(writeValues), 'echo:',echo)
            return False

    def check(self):
        if self.driveBoat(0,0,0):
            self.controllable = True
        else:
            self.controllable = False
        
        if self.debug:
            print('Check:', self.controllable)

    def driveBoat(self, motorL, motorR, rudder):
        self.driveMotor(motorL,motorR)
        self.driveRudder(rudder)
        return self.write()

    def driveMotor(self, motorL, motorR):
        tmp = motorL
        motorL = motorR
        motorR = tmp
        motorL = motorL * 100
        motorR = motorR * 100
        motorL = np.clip(motorL,-100,100) / 2
        motorR = np.clip(motorR,-100,100) / 2
        
        self.motorL=90+motorL
        self.motorR=90+motorR


    def driveRudder(self, angle):
        angle = angle * -1 # Reverse angle value
        angle = angle * 100
        angle = np.clip(angle, -100, 100) / 2
        self.rudderL = self.rudderR = 90 + angle

    
