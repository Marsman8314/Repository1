import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 100
sampling_frequency = 10000

if __name__ == "__main__":
    dac = None
    try:
        dac = mcp.MCP4725(dynamic_range=5.0,
                          address=0x61,
                          verbose=False)

        start_time = time.time()
        while True:
            t = time.time() - start_time
            normalized = sg.get_triangle_wave_amplitude(signal_frequency, t)
            voltage = normalized * amplitude
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)

    finally:
        if dac is not None:
            dac.deinit()