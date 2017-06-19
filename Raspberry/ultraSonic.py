from __future__ import print_function
import time
import RPi.GPIO as GPIO
import atexit


def exit_handler():
    GPIO.cleanup()


class Ping:
    def __init__(self, temperature=20):
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

        # Calculate the difference in time
        elapsed = stop - start
        # Calculate the measured distance
        distance = (elapsed * self.speedSound) / 2

        # Wait 20ms
        time.sleep(0.02)
        return distance

def test():
    p = Ping()
    while True:
        print(p.measure(0),p.measure(1),p.measure(2))

#test()

