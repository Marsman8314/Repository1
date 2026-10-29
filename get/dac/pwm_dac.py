import RPi.GPIO as GPIO


class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        """
        gpio_pin       — номер GPIO-пина (BCM), на котором генерируется ШИМ
        pwm_frequency  — частота ШИМ в Герцах
        dynamic_range  — напряжение питания (максимум на выходе), В
        verbose        — печатать ли отладочную информацию
        """
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial=0)

        # Создаём объект ШИМ с заданной частотой
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)   # старт с duty cycle = 0%

    def deinit(self):
        """Останавливает ШИМ и сбрасывает настройки GPIO."""
        self.pwm.stop()
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        """Выставляет напряжение на выходе ЦАП на ШИМ."""
        if not isinstance(voltage, (int, float)):
            print("Напряжение должно быть числом")
            return

        # Ограничиваем напряжение динамическим диапазоном
        if voltage < 0:
            voltage = 0
        elif voltage > self.dynamic_range:
            voltage = self.dynamic_range

        # duty cycle в процентах: 0..100
        duty_cycle = (voltage / self.dynamic_range) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(f"Напряжение: {voltage:.3f} В, "
                  f"duty cycle: {duty_cycle:.2f}%\n")


if __name__ == "__main__":
    dac = None
    try:
        dac = PWM_DAC(gpio_pin=12,
                      pwm_frequency=500,
                      dynamic_range=3.290,
                      verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        if dac is not None:
            dac.deinit()