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
        # Подтяжка на всякий случай — если компаратор с открытым коллектором
        GPIO.setup(self.comp_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __del__(self):
        try:
            self.number_to_dac(0)
        finally:
            GPIO.cleanup()

    def number_to_dac(self, number):
        for i in range(8):
            bit = (number >> i) & 1
            GPIO.output(self.bits_gpio[i], bit)

    # ---------- АЦП последовательного счёта ----------
    def sequential_counting_adc(self):
        # Ищем первое число, при котором ЦАП СТРОГО превысил вход (comp == 1)
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"[SC] Компаратор сработал на числе {number}")
                return number
        return 255

    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"[SC] Код: {code}, напряжение: {voltage:.3f} В")
        return voltage

    # ---------- АЦП последовательного приближения ----------
    def successive_approximation_adc(self):
        code = 0
        for bit in range(7, -1, -1):
            trial = code | (1 << bit)
            self.number_to_dac(trial)
            time.sleep(self.compare_time)

            # comp == 1 означает ЦАП > вход → бит слишком велик, сбрасываем
            # comp == 0 означает ЦАП <= вход → бит оставляем
            if GPIO.input(self.comp_gpio) == 0:
                code = trial

            if self.verbose:
                print(f"[SAR] Бит {bit}: пробуем {trial}, comp={GPIO.input(self.comp_gpio)}, оставляем {code}")

        if self.verbose:
            print(f"[SAR] Итоговый код: {code}")
        return code

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"[SAR] Код: {code}, напряжение: {voltage:.3f} В")
        return voltage


if __name__ == "__main__":
    adc = None
    try:
        # dynamic_range — реальный максимум ЦАП, измеренный мультиметром при коде 255
        # compare_time=0.01 — НЕ МЕНЬШЕ, иначе компаратор не успевает
        adc = R2R_ADC(dynamic_range=3.3, compare_time=0.01, verbose=False)
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        if adc is not None:
            adc.__del__()