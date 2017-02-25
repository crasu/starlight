from machine import Timer
import time
import machine

INTERVAL = 1000

class AlarmHandler:
    i=0
    duty_cycle = {}
    p_out = {}
    enable = True

    @classmethod
    def pwm(self, i):
        pass

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
