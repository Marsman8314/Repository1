import pwm_dac2 as pwm
import signal_generator as sg
import time
amplitude = 3
signal_frequency = 100
sampling_frequency = 10000000
if __name__ == "__main__":
    dac = None
    try:
        dac = pwm.PWM_DAC(gpio_pin=12,
                          pwm_frequency=500,
                          dynamic_range=3.290,
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