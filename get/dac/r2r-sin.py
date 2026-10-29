import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 3
signal_frequency = 40
sampling_frequency = 20000
try:
    dac = r2r.R2R_DAC([16,20,21,25,26,17,27,22],3.15)
    start_time = time.time()
    while True:
        xtime = time.time() - start_time
        value = sg.get_sin_wave_amplitude(signal_frequency, xtime)
        dac.set_voltage(value * amplitude)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()