from machine import Pin
from time import sleep

# Connect to Solenoid for test if you need
print("Test Start")

relay = Pin(18, Pin.OUT, value=1)  # default OFF (LOW trigger) , value=1

while True:
    relay.value(0)   # ON
    sleep(1)
    relay.value(1)   # OFF
    sleep(1)