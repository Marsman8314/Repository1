import RPi.GPIO as GPIO
import time
from r2r_adc import R2R_ADC

adc = R2R_ADC(dynamic_range=3.3, compare_time=0.01)
# все пины, кроме занятых ЦАП
free_pins = [p for p in range(2, 28) if p not in adc.bits_gpio]
for p in free_pins:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Крутите потенциометр, смотрю какие пины меняются...")
prev = {p: GPIO.input(p) for p in free_pins}
for _ in range(200):
    adc.number_to_dac(0); time.sleep(0.02)
    adc.number_to_dac(255); time.sleep(0.02)
    for p in free_pins:
        v = GPIO.input(p)
        if v != prev[p]:
            print(f"Пин {p} изменился: {prev[p]} -> {v}")
            prev[p] = v
adc.__del__()