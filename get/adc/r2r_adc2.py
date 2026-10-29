import RPi.GPIO as GPIO
import time
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
    def __del__(self):
        self.number_to_dac(0)
        GPIO.cleanup()
    def number_to_dac(self, number):
        for i in range(8):
            bit = (number >> i) & 1
            GPIO.output(self.bits_gpio[i], bit)
    # --- АЦП последовательного счёта (из прошлого задания) ---
    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"Компаратор сработал на числе {number}")
                return number
        return 255
    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"Код: {code}, напряжение: {voltage:.3f} В")
        return voltage

    # --- АЦП последовательного приближения (новое) ---
    def successive_approximation_adc(self):
        code = 0
        for bit in range(7, -1, -1):
            trial = code | (1 << bit)
            self.number_to_dac(trial)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == 0:
                # ЦАП <= вход, бит оставляем
                code = trial
            if self.verbose:
                print(f"Бит {bit}: пробуем {trial}, оставляем {code}")
        if self.verbose:
            print(f"Итоговый код: {code}")
        return code
    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"Код: {code}, напряжение: {voltage:.3f} В")
        return voltage
if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.3, verbose=True)
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        adc.__del__()