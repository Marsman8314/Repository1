import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led,GPIO.OUT)
state = 0
rez = 6
GPIO.setup(rez, GPIO.IN)
while True:
    if GPIO.input(rez) == 1:
        #state = not state
        GPIO.output(led,0)
        #time.sleep(1)
    else:
       GPIO.output(led,1) 