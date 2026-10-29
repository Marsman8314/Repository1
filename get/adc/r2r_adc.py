import time
import RPi.GPIO as GPIO
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        time.sleep(0.01)
        GPIO.cleanup()
    def __del__(self):
        try:
            self.deinit()
        except Exception:
            pass
    def number_to_dac(self, number):
        for i in range(8):
            bit = (number >> (7 - i)) & 1
            GPIO.output(self.bits_gpio[i], bit)

    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                return number
        return 255
    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        return code * self.dynamic_range / 255.0
if __name__ == "__main__":
    adc = None
    try:
        adc = R2R_ADC(dynamic_range=3.3, verbose=False)
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение: {voltage:.3f} В", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nЗавершение работы", flush=True)
    finally:
        if adc is not None:
            adc.deinit()