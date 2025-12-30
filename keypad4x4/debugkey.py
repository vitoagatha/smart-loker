from machine import Pin
from time import sleep

row_pins = [10, 11, 12, 13]
col_pins = [14, 15, 16, 17]

rows = [Pin(p, Pin.OUT) for p in row_pins]
cols = [Pin(p, Pin.IN, Pin.PULL_UP) for p in col_pins]

for r in rows:
    r.value(1)

print("DEBUG MODE")

while True:
    for r in range(4):
        rows[r].value(0)
        for c in range(4):
            if cols[c].value() == 0:
                print("ROW", r, "COL", c)
                sleep(0.3)
        rows[r].value(1)
