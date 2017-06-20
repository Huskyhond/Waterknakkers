from __future__ import print_function
import time
import RPi.GPIO as GPIO
import atexit


def exit_handler():
    GPIO.cleanup()


class Ping:
    def __init__(self, temperature=20, smoothingRange = 20):
        self.smoothingRange = smoothingRange
        self.prevValues = []
        self.spikeValues = []
        # Use BCM GPIO references, instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Define GPIO to use on Pi
        # [[Trig,Echo],] GPIO references for the (3)ultra sonic sensors
        self.GPIO_PINS = [[17, 27], [23, 24], [25,8]]

        # Speed of sound in cm/s at temperature
        self.temperature = temperature
        self.speedSound = 33100 + (0.6 * self.temperature)

        print("Speed of sound is", self.speedSound / 100, "m/s at ", self.temperature, "deg")

        # Set pins as output and input
        GPIO.setup(self.GPIO_PINS[0][0], GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_PINS[0][1], GPIO.IN)   # Echo

        GPIO.setup(self.GPIO_PINS[1][0], GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_PINS[1][1], GPIO.IN)   # Echo

        GPIO.setup(self.GPIO_PINS[2][0], GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_PINS[2][1], GPIO.IN)   # Echo

        # Set triggers to False (LOW)
        GPIO.output(self.GPIO_PINS[0][0], False)
        GPIO.output(self.GPIO_PINS[1][0], False)
        GPIO.output(self.GPIO_PINS[2][0], False)

        # Set cleanup at exit
        atexit.register(exit_handler)

        # Allow module to settle
        time.sleep(0.5)

    def measure(self, sensor):
        # Set trigger to True (HIGH)
        GPIO.output(self.GPIO_PINS[sensor][0], True)
        # Wait 10us
        time.sleep(0.00001)
        # Set trigger to False (LOW)
        GPIO.output(self.GPIO_PINS[sensor][0], False)
        start = time.time()

        # Wait for the echo pin to set to LOW
        while GPIO.input(self.GPIO_PINS[sensor][1]) == 0:
            start = time.time()

        # Wait for the echo pin to set to HIGH
        while GPIO.input(self.GPIO_PINS[sensor][1]) == 1:
            stop = time.time()
            # Timeout after 0.2s
            if stop > 0.2:
                return 0

        # Calculate the difference in time
        elapsed = stop - start
        # Calculate the measured distance
        distance = self.smoothDistance((elapsed * self.speedSound) / 2)
        # Wait 20ms
        time.sleep(0.02)
        return distance

    def smoothDistance(self, distance):
        if len(self.prevValues) > 0 and abs(distance-self.prevValues[len(self.prevValues)-1]) > self.smoothingRange:
            self.spikeValues.append(distance)
            if len(self.spikeValues) is spikeSize:
                self.prevValues += self.spikeValues[:spikeSize-1]
                #print(self.spikeValues)
                for pV in self.prevValues:
                    if len(self.prevValues) is bufferSize-1: break
                    else: self.prevValues.pop(0)
                self.spikeValues = []
            else:
                continue
        else:
            self.spikeValues = []
            
        self.prevValues.append(distance)
        if len(self.prevValues) is bufferSize+1:
            self.prevValues.pop(0)
        #print(distance,self.prevValues,sum(self.prevValues)/len(self.prevValues))
        return sum(self.prevValues)/len(self.prevValues)

def test():
    p = Ping()
    while True:
        print(p.measure(0),p.measure(1),p.measure(2))

#test()

