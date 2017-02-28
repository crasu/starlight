import machine
import _thread
import utime

from server import PINS

divider = 5
enable=True
outputs = { pin: machine.Pin(pin, mode=machine.Pin.OUT) for pin in PINS }
for output in outputs:
    output = False

duty_cycle = {}

def run():
    global enable
    i = 0
    while enable:
        i = (i + 1) % 10000
        for pin in duty_cycle:
            on = False

            if duty_cycle[pin] <= 0 or duty_cycle[pin] >= 100:
                on = duty_cycle[pin] >= 100
            else:
                if duty_cycle[pin] < 50:
                    on = i % (100//duty_cycle[pin]) == 0
                else:
                    on = i % (100//(100-duty_cycle[pin])) != 0

            outputs[pin](on)

    print("terminating")

def start():
    global enable
    enable = True
    _thread.start_new_thread(run, ())
    for j in range(1,101,10):
        print(j)
        duty_cycle['P9'] = j
        utime.sleep_ms(3000)
    enable = False
    utime.sleep(3)
