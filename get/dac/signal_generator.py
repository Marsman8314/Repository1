import numpy as np
import time
def get_sin_wave_amplitude(freq, time):
    s = np.sin(2*np.pi*freq*time)
    return ((s+1)/2)
def get_triangle_wave_amplitude(freq, time_moment):
    period = 1.0 / freq
    phase = (time_moment % period) / period
    if phase < 0.5:
        return phase * 2
    else:
        return (1 - phase) * 2
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/(sampling_frequency))