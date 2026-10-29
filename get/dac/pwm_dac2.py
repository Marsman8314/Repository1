import RPi.GPIO as GPIO
import time


class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.pin = gpio_pin
        self.freq = pwm_frequency
        self.range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(0)
        if self.verbose:
            print("PWM_DAC создан на пине", self.pin)

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()
        if self.verbose:
            print("PWM_DAC остановлен")

    def set_voltage(self, voltage):
        if voltage < 0:
            voltage = 0
            print(f"Выходит за динамический диапазон {self.range} B")
            print("выставляем напряжение 0")
            return 0
        if voltage > self.range:
            voltage = self.range
            print(f'Выход за динамический диапазон {self.range} В')
            return 0
        duty = (voltage / self.range) * 100
        self.pwm.ChangeDutyCycle(duty)
        if self.verbose:
            print("Напряжение:", voltage, "В, скважность:", duty, "%")


if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.295, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
