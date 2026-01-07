#final pin test open solenoid
from machine import Pin, SoftI2C
from time import sleep
from pico_i2c_lcd import I2cLcd

#LCD
i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.clear()
lcd.putstr("Smart Locker\nReady")
sleep(2)
lcd.clear()
lcd.putstr("Masukkan PIN:")

relay = Pin(18, Pin.OUT)
RELAY_ACTIVE_LOW = True #True

def relay_on():
    relay.value(0 if RELAY_ACTIVE_LOW else 1)

def relay_off():
    relay.value(1 if RELAY_ACTIVE_LOW else 0)

relay_off()  # Solenoid close

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

def scan_key():
    for r in range(4):
        for rr in rows:
            rr.value(1)
        rows[r].value(0)
        sleep(0.005)

        for c in range(4):
            if cols[c].value() == 0:
                sleep(0.02)
                while cols[c].value() == 0:
                    sleep(0.01)
                return keys[r][c]
    return None

#PIN
PASSWORD = "2580"
buf = ""
MAX_LEN = 8
UNLOCK_SEC = 5

def show_prompt():
    lcd.clear()
    lcd.putstr("Masukkan PIN:")

show_prompt()

while True:
    k = scan_key()
    if not k:
        continue

    if k == '*':  # clear
        buf = ""
        show_prompt()

    elif k == '#':  # submit
        if buf == PASSWORD:
            lcd.clear()
            lcd.putstr("PIN Benar\nMembuka...")
            relay_on()
            sleep(UNLOCK_SEC)
            relay_off()
            buf = ""
            lcd.clear()
            lcd.putstr("Tertutup\nMasukkan PIN:")
        else:
            lcd.clear()
            lcd.putstr("PIN Salah\nCoba lagi")
            sleep(1)
            buf = ""
            show_prompt()

    else:
        if len(buf) < MAX_LEN:
            buf += k
        # * for hide pin
        lcd.clear()
        lcd.putstr("PIN: " + ("*" * len(buf)))
        lcd.putstr("\n#=OK *=Hapus")