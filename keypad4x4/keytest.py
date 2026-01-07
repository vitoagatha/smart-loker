from machine import Pin, SoftI2C
from time import sleep
from pico_i2c_lcd import I2cLcd

#LCD
I2C_ADDR = 0x27
I2C_ROWS = 2
I2C_COLS = 16

i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_ROWS, I2C_COLS)

lcd.clear()
lcd.putstr("KEYPAD READY")

#KEYPAD
keys = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']
]

row_pins = [10, 11, 12, 13]
col_pins = [14, 15, 16, 17]

rows = [Pin(p, Pin.OUT) for p in row_pins]
cols = [Pin(p, Pin.IN, Pin.PULL_UP) for p in col_pins]

for r in rows:
    r.value(1)

def scan():
    for r in range(4):
        rows[r].value(0)
        for c in range(4):
            if cols[c].value() == 0:
                rows[r].value(1)
                return keys[r][c]
        rows[r].value(1)
    return None

buffer = ""

while True:
    k = scan()
    if k:
        if k == '*':
            buffer = ""
            lcd.clear()
            lcd.putstr("Cleared")
        elif k == '#':
            lcd.clear()
            lcd.putstr("Input:\n" + buffer)
        else:
            buffer += k
            lcd.clear()
            lcd.putstr("Input:\n" + buffer)

        print("Pressed:", k)
        sleep(0.3)