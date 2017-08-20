import RPi.GPIO as GPIO
from pinMeta import activePins;
from pinMeta import allValidPins;
GPIO.setmode(GPIO.BOARD)

#Inactive pins:
inactivePins = [];
for pin in allValidPins:
	if(pin not in activePinsMap):
		print(str(pin) + " is inactive");

#Initialize ALL pins as low out:
def configureAllPinsLow():
    print ('Configuring all pins low out');
    for x in range(0,len(allValidPins)):
        try:
            GPIO.setup(allValidPins[x], GPIO.OUT);
            GPIO.output(allValidPins[x], False);
        except Exception as e:
            print (str(e) + ': ' + str(activePins[x]));
    print ('Finished configuring pins');

configureAllPinsLow();