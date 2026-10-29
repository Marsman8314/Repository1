import mcp4725_driver as mcp
import signal_generator as sg
import time


# Параметры генерируемого сигнала (задаются здесь, не через input)
amplitude = 3.2             # амплитуда в Вольтах
signal_frequency = 10       # частота сигнала в Герцах
sampling_frequency = 1000   # частота дискретизации в Герцах


if __name__ == "__main__":
    dac = None
    try:
        dac = mcp.MCP4725(dynamic_range=5.0, address=0x61, verbose=False)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        if dac is not None:
            dac.deinit()