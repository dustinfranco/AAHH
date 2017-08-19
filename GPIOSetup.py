import RPi.GPIO as GPIO
from pinMeta import activePins;
from pinMeta import allValidPins;
GPIO.setmode(GPIO.BOARD)

#All pins
allValidPins = [\
8 ,10,12,16,18,22,\
24,26,32,36,38,40,\
3 , 5, 7,11,13,15,\
19,21,23,29,31,33,\
35,37];

#Pins mapped to guitar notes
activePins = [\
 8, 16,12, 5,10,11,\
13,22,3, 7,15,21,\
40,18,24,22,38,26,\
33,35,37,31,32,36,
 0, 0, 0, 0, 0, 0]

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