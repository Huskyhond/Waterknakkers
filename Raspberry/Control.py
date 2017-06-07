import serial
from time import sleep
import numpy as np
from pyparsing import*

class Control:
    def __init__(self, port='/dev/ttyACM0',baudrate=115200):
        try:
            self.ser=serial.Serial(port,baudrate)
            print('Serial port opened at:',port, 'baudrate:', baudrate)
            print("Sleep...")
            sleep(3)
            print(self.ser.read(self.ser.inWaiting()))
            self.connected = True   
        except:
            print('Opening Serial port failed, try again or try another port.')
            self.connected = False

        self.motorL=90
        self.motorR=90
        self.rudderL=90
        self.rudderR=90
        self.prev=0

    def write(self):
        """
            Write values to arduino
            LR,RR,LM,RM
        """
        #constructs a string to send to the arduino
        string = 'a'+str(int(self.rudderL))+'b'+str(int(self.rudderR))+'c'+str(int(self.motorL))+'d'+str(int(self.motorR))+'z'
        #send string to arduino
        print('write:',string)
        self.ser.write(string)
        #wait 10 ms
        sleep(0.01)
        #print the data that was send to the arduino
        #print('Data naar arduino:', string)
        # read and print the echo from the arduino
        echo=self.ser.read(self.ser.inWaiting())
        print('echo:',echo)
        #print('Data van arduino terug:',echo)
        # check is the echo is equal to the data send to the arduino

        test=Literal('a')+Word(nums)+Literal('b')+Word(nums)+Literal('c')+Word(nums)+Literal('d')+Word(nums)+Literal('z')

        try:
            antwoord=test.parseString(echo)
        except:
            #no data received from arduino, or incorrect format
            print('Incorrect or empty echo from arduino received')
            return 0

        results=[int(antwoord[1]),int(antwoord[3]),int(antwoord[5]),int(antwoord[7])]
        waardes=[int(self.rudderL),int(self.rudderR),int(self.motorL),int(self.motorR)]
        
        if (results==waardes):
            #correct data received from arduino
            if (self.prev!=results):
                #print(results)
                self.prev=results
            return 1
        else:
            #data received from arduino was of correct format, but not correct values
            print('Incorrect echo from arduino received')
            return 0


    def Motor(self, motorL, motorR):
        motorL = motorL * 100
        motorR = motorR * 100
        motorL = np.clip(motorL,-100,100) / 2
        motorR = np.clip(motorR,-100,100) / 2
        
        self.motorL=90+motorL
        self.motorR=90+motorR
        print("L:",self.motorL,"R:",self.motorR)

        self.write()


    def Rudder(self, angle):
        angle = angle * 100
        angle = np.clip(angle, -100, 100) / 2
        self.rudderL = self.rudderR = 90 + angle
        self.write()

    