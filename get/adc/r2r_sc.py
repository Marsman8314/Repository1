import time
from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist
voltage_values = []
time_values = []
# Продолжительность измерений (с)
duration = 5.0
dynamic_range = 3.3
adc = None
try:
    adc = R2R_ADC(dynamic_range=dynamic_range, compare_time=0.0001)
    start_time = time.time()
    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sc_voltage())
        time_values.append(time.time() - start_time)
    plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
    plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nИзмерения прерваны пользователем")
finally:
    if adc is not None:
        adc.__del__()