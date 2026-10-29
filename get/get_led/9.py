import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16,12,25,17,27,23,22,24]
GPIO.setup(leds,GPIO.OUT)
up = 9
GPIO.setup(up, GPIO.OUT)
down = 10
GPIO.setup(down, GPIO.OUT)
num = 0
a = [0]*8
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(11)]
sleep_time = 0.2
print(dec2bin(227))
while True:
    if GPIO.input(up):
        num+=1
        if num>256:
            num=256
        a = dec2bin(num)
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if GPIO.input(down):
        num-=1
        if num<0:
            num=0
        a = dec2bin(num)
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if GPIO.input(down) and GPIO.input(up):
        a = [1,1,1,1,1,1,1,1]
        time.sleep(sleep_time)
    GPIO.output(leds, a)
    #if GPIO.input(down) and GPIO.input(up):
        #GPIO.output(leds, 1)
