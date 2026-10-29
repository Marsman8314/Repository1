import pwm_dac2 as pwm
import signal_generator as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
try:
    dac = pwm.PWM_DAC(12, 500, 3.295, True)
    start_time = time.time()
    while True:
        xtime = time.time() - start_time
        value = sg.get_sin_wave_amplitude(signal_frequency, xtime)
        dac.set_voltage(value * amplitude)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()