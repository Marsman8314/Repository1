import time
from r2r_adc import R2R_ADC
import adc_plot2
# Замените 3.3 на реальный динамический диапазон вашего ЦАП,
# измеренный мультиметром
DYNAMIC_RANGE = 3.3
DURATION = 10
adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.0001)
voltage_values = []
time_values = []
try:
    start_time = time.time()
    while time.time() - start_time < DURATION:
        voltage_values.append(adc.get_sc_voltage())
        time_values.append(time.time() - start_time)
    adc_plot2.plot_voltage_vs_time(time_values,voltage_values,DYNAMIC_RANGE)
    adc_plot2.plot_sampling_period_hist(time_values)
finally:
    adc.deinit()