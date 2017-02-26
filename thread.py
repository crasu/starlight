import machine
import _thread
import time

from server import PINS

class Pwm:
    i=0
    enable=True
    output = { pin: machine.Pin(pin, mode=machine.Pin.OUT) for pin in PINS }
    duty_cycle = {}
    
    def __init__(self):
        pass

    @classmethod
    def run(cls):
        while cls.enable:
            cls.i = (cls.i + 1) % 100
            duty_cycle = cls.duty_cycle

            for pin in duty_cycle:
                on = False
                if duty_cycle[pin] <= 0 or duty_cycle[pin] >= 100:
                    on = duty_cycle[pin] >= 100
                else:
                    if duty_cycle[pin] < 50:
                        on = cls.i % (100/duty_cycle[pin]) == 0
                    else:
                        on = cls.i % (100/(100-duty_cycle[pin])) != 0
                cls.output[pin] = on
        print("terminating")
            

    @classmethod
    def stop(cls):
        cls.enable = False
    
    @classmethod
    def set_duty_cycle(cls, pin, value):
        cls.duty_cycle[pin] = value

def start():
    _thread.start_new_thread(Pwm.run, ())
    Pwm.duty_cycle['P9'] = 20
    print("sleep")
    time.sleep(5)
    print("cycle 90")
    Pwm.duty_cycle['P9'] = 90


