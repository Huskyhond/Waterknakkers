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
            print('er ging iets mis')
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
            print('niet zo succesvol')
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

    '''
    def Forwards(self, speed):
        """
            Puts the motors in forward motion
        """
        speed=np.clip(speed,0,100)
        self.motorL=90+(speed/100.*50.)
        self.motorR=90+(speed/100.*50.)
        self.write()

    def Backwards(self, speed):
        """
            Puts the motors in backwards motion
        """
        speed=np.clip(speed,0,100)
        self.motorL=90-(speed/100.*50.)
        self.motorR=90-(speed/100.*50.)
        self.write()

    def SteerLeft(self, steer):
        """
            Steers the servos left
        """
        steer=np.clip(steer,0,100)
        self.rudderL=90+(steer/100.*50.)
        self.rudderR=90+(steer/100.*50.)
        self.write()

    def SteerRight(self, steer):
        """
            Steers the servos right
        """
        steer=np.clip(steer,0,100)
        self.rudderL=90-(steer/100.*50.)
        self.rudderR=90-(steer/100.*50.)
        self.write()

    def RotateRight(self,speed):
        """
            Rotates the boat by counterspinning the engines
        """
        speed=np.clip(speed,0,100)
        self.motorL=90-(speed/100.*50.)
        self.motorR=90+(speed/100.*50.)
        self.write()

    def RotateLeft(self,speed):
        """
            Rotates the boat by counterspinning the engines
        """
        speed=np.clip(speed,0,100)
        self.motorL=90+(speed/100.*50.)
        self.motorR=90-(speed/100.*50.)
        self.write()

    def SteerDeg(self,steer):
        """
            Steers the rudders by a certain deg
        """
        steer=np.clip(steer,-45,45)+90
        self.rudderL=steer
        self.rudderR=steer
        self.write()
    '''

    