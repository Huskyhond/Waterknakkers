from __future__ import print_function
import time
import RPi.GPIO as GPIO
import atexit

# The function being executed when the programs exits
def exit_handler():
    GPIO.cleanup()

class Ping:
    def __init__(self, temperature=20, smoothingRange = 20):
        self.smoothingRange = smoothingRange    # The range that determines if a distance is considered a spike value
                                                # Example: incoming sensor distances = [10,11,9,15,40,45,12,11]
                                                # 40 and 45 are out of the smoothing range and are considered spikes and will be ignored
        self.prevValues = [[],[],[]]            # The list which stores the last 4 distances of each sensor
        self.spikeValues = [[],[],[]]           # The list which stores the last 4 spikes of each sensor
        # Use BCM GPIO references, instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Define GPIO to use on Pi
        # [[Trig,Echo],] GPIO references for the (3)ultra sonic sensors
        self.GPIO_PINS = [[17, 27], [23, 24], [25,8]]

        # Speed of sound in cm/s at temperature
        self.temperature = temperature
        self.speedSound = 33100 + (0.6 * self.temperature)

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

    # Change temperature value and calculate speed of sound
    def setTemperature(self,temperature):
        self.temperature = temperature
        self.speedSound = 33100 + (0.6 * self.temperature)
        print("Speed of sound is", self.speedSound / 100, "m/s at ", self.temperature, "deg")

    # Calculate the distance from the sensor to the object
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
            if stop - start > 0.2:
                return 0

        # Calculate the difference in time
        elapsed = stop - start
        # Calculate the measured distance
        distance = (elapsed*self.speedSound )/2
        distance = self.smoothDistance(distance, sensor)
        # Wait 20ms
        time.sleep(0.02)
        return distance

    # Smooth distance values
    def smoothDistance(self, distance, sensor):
        # This function smooths the incoming sensor values by calculating the average of the last 4 values
        # If a incoming distance is out of the smoothing range, it will be ignored and added to the spikeValues list
        # If the spikes continue 4 times in succession, then the spikeValues will be considered as real distance values

        bufferSize = 4
        spikeSize = 4
        if len(self.prevValues[sensor]) > 0 and abs(distance-self.prevValues[sensor][len(self.prevValues[sensor])-1]) > self.smoothingRange:
            self.spikeValues[sensor].append(distance)
            if len(self.spikeValues[sensor]) is spikeSize:
                self.prevValues[sensor] += self.spikeValues[sensor][:spikeSize-1]
                #print(self.spikeValues[sensor])
                for pV in self.prevValues[sensor]:
                    if len(self.prevValues[sensor]) is bufferSize-1: break
                    else: self.prevValues[sensor].pop(0)
                self.spikeValues[sensor] = []
            else:
                return sum(self.prevValues[sensor])/len(self.prevValues[sensor])
        else:
            self.spikeValues[sensor] = []
            
        self.prevValues[sensor].append(distance)
        if len(self.prevValues[sensor]) is bufferSize+1:
            self.prevValues[sensor].pop(0)
        return sum(self.prevValues[sensor])/len(self.prevValues[sensor])

# Test function
def test():
    p = Ping()
    while True:
        print(p.measure(0),p.measure(1),p.measure(2))

#test()

