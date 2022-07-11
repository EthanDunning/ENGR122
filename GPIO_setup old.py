from time import *
import RPi.GPIO as GPIO

# pins
leds = [17, 16, 13, 12]
switches = [18, 19, 20, 21]
wires = []
sonic_sensor = []
test_led = []


# setting up the GPIO
GPIO.setmode(GPIO.BCM)
# I/O
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(test_led, GPIO.OUT)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(wires, GPIO.IN)


# testing the leds
def all_on():
    for i in leds:
        GPIO.output(leds, True)

def all_off():
    for i in leds:
        GPIO.output(leds, False)

def switch_test():
    for i in switches:
        if i == True:
            GPIO.output(test_led, True)



all_on()
sleep(0.5)
all_off()
sleep(0.5)

# ultrasonic sensor
GPIO_TRIGGER = []
GPIO_ECHO = None
 
# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
 

