from machine import Timer
import time
import machine

INTERVAL = 50000

class AlarmHandler:
    i=0
    duty_cycle = {}
    p_out = {}
    enable = True

    @classmethod
    def pwm(self, i):
        duty_cycle = self.duty_cycle

        for pin in duty_cycle:
            on = False
            if duty_cycle[pin] == 0 or duty_cycle[pin] == 100:
                on = duty_cycle[pin] == 100
            else:
                if duty_cycle[pin] < 50:
                    on = i % (100//duty_cycle[pin]) == 0
                else:
                    on = i % (100//(100-duty_cycle[pin])) != 0
            #print("Pin: {} is {} for i={}".format(pin, on, i))
            self.p_out[pin](on)

    @classmethod
    def handler(self, alarm):
        if self.enable == False:
            return

        self.i=self.i+1
        self.i=self.i % 100

        self.pwm(self.i)

    @classmethod
    def disable(self):
        self.enable = False
        print("alarm disabled")

    @classmethod
    def enable(self):
        self.enable = True
        print("alarm enabled")

    @classmethod
    def set_duty_cycle(self, pin, value):
        self.duty_cycle[pin] = value
        self.p_out[pin] = machine.Pin(pin, mode=machine.Pin.OUT)  


alarm = Timer.Alarm(AlarmHandler.handler, us=INTERVAL, periodic=True)
AlarmHandler.set_duty_cycle('P9', 99)
