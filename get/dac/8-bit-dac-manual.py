import RPi.GPIO as GPIO
#import time
GPIO.setmode(GPIO.BCM)
leds = [16,20,21,25,26,17,27,22]
#leds = [22,27,17,26,25,21,20,16]
GPIO.setup(leds,GPIO.OUT)
dynamic_range = 3.158
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Выходит за динамический диапазон ЦАП (0.0 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage/dynamic_range *256)
def number_to_dac(number):
    Arr = [int(element) for element in bin(number)[2:].zfill(8)]
    GPIO.output(leds,Arr)
try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах :"))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except ValueError:
            print("Вы ввели не число\n")
finally:
    GPIO.output(leds,0)
    GPIO.cleanup()