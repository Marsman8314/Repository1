import smbus
import math


class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00          # Write Mode: 00 = запись в DAC-регистр
        self.pds = 0x00         # Power-Down Mode: 00 = нормальный режим
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        """Закрывает шину I2C."""
        self.bus.close()

    def set_number(self, number):
        """Отправляет 12-битное число в MCP4725 по I2C."""
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF

        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(
                f"Число: {number}, отправленные по I2C данные: "
                f"[0x{(self.address << 1):02X}, "
                f"0x{first_byte:02X}, 0x{second_byte:02X}]\n"
            )

    def set_voltage(self, voltage):
        """Выставляет напряжение на выходе MCP4725."""
        if not isinstance(voltage, (int, float)) or not math.isfinite(voltage):
            print("Напряжение должно быть конечным числом")
            return

        if voltage < 0:
            voltage = 0
        elif voltage > self.dynamic_range:
            voltage = self.dynamic_range

        number = int((voltage / self.dynamic_range) * 4095)
        self.set_number(number)


if __name__ == "__main__":
    dac = None
    try:
        dac = MCP4725(dynamic_range=5.0, address=0x61, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        if dac is not None:
            dac.deinit()