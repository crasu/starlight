from machine import Timer
import time

INTERVAL = 1000000

class AlarmHandler:
    i=0
    duty_cycle = {}
    enable = True

    @classmethod
    def pwm(self, i, duty_cycle):
        duty_cycle = self.duty_cycle

        for pin in duty_cycle:
            if duty_cycle[pin] == 0 or duty_cycle[pin] == 100:
                on = duty_cycle[pin] == 100
            else:
                on = False
                if duty_cycle[pin] < 50:
                    on = i % (100/duty_cycle[pin]) == 0
                else:
                    on = i % (100/(100-duty_cycle[pin])) == 0
            print("Pin: {} is {}".format(pin, on))

    @classmethod
    def handler(self, alarm):
        if self.enable == False:
            print("alarm disabled")
            alarm.__del__()
            return

        self.i=self.i+1
        self.i=self.i % 100

        self.pwm(self.i)

    @classmethod
    def disable(self):
        self.enable = False

    @classmethod
    def enable(self):
        self.enable = True

    @classmethod
    def set_duty_cycle(self, pin, value):
        self.duty_cycle[pin] = value


alarm = Timer.Alarm(AlarmHandler.handler, us=INTERVAL, periodic=True)
