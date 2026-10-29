import RPi.GPIO as GPIO
class R2R_DAC:
    def __init__(self, gpio_bits, dynaminc_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynaminc_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    def set_number(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    def set_voltage(self, voltage):
        if not(0<=voltage<=self.dynamic_range):
            print(f"Выходит за динамический диапазон ЦАП (0.0 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем напряжение 0.0 В")
            GPIO.output(self.gpio_bits, self.set_number(0))
            return 0
        number = int(voltage/self.dynamic_range*256)
        GPIO.output(self.gpio_bits, self.set_number(number))
if __name__ == "__main__":
    try:
        dac = R2R_DAC([16,20,21,25,26,17,27,22],3.158,True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)#######
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё разок :)\n")
    finally:
        dac.deinit()