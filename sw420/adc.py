import machine
from machine import ADC
import time

adc = ADC(3)

while True:
    adc_value = adc.read_u16()
    print('Adc_value:',adc_value)
    time.sleep(0.2)