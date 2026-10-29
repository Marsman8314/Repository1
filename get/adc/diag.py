import time
import RPi.GPIO as GPIO

pins = [26, 20, 19, 16, 13, 12, 25, 11]
comp = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)

def set_num(n, reverse=False):
    for i in range(8):
        shift = (7 - i) if reverse else i
        GPIO.output(pins[i], (n >> shift) & 1)

try:
    for reverse in [False, True]:
        print(f"\n--- reverse={reverse} ---", flush=True)
        found = None
        for n in range(256):
            set_num(n, reverse)
            time.sleep(0.01)
            if GPIO.input(comp) == 1:
                found = n
                break
        print(f"Компаратор сработал на number={found}", flush=True)
        set_num(0)
        time.sleep(0.2)
finally:
    GPIO.output(pins, 0)
    GPIO.cleanup()