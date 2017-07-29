import GPIOSetup.py
import time

def testPin(inputPin, timeOn):
    GPIO.output(inputPin, True)
    time.sleep(timeOn)
    GPIO.output(inputPin, False)
