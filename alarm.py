from machine import Timer
import time

INTERVAL = 1000000

class AlarmHandler:
    i=0
    duty_cycle = {}
    enable = True

    @classmethod
    def pwm(cls, i, duty_cycle):
        duty_cycle = cls.duty_cycle

        for pin in duty_cycle:
            if duty_cycle[pin] == 0 or duty_cycle[pin] == 100:
                on = duty_cycle[pin] == 100
            else:
                on = False
                if duty_cycle[pin] < 50:
                    on = i % (100/duty_cycle[pin]) == 0
                else:
                    on = i % (100/(100-duty_cycle[pin])) != 0
            print("Pin: {} is {}".format(pin, on))

    @classmethod
    def handler(cls, alarm):
        if cls.enable == False:
            print("alarm disabled")
            alarm.__del__()
            return

        cls.i=cls.i+1
        cls.i=cls.i % 100

        cls.pwm(cls.i)

    @classmethod
    def disable(cls):
        cls.enable = False

    @classmethod
    def enable(cls):
        cls.enable = True

    @classmethod
    def set_duty_cycle(cls, pin, value):
        cls.duty_cycle[pin] = value


alarm = Timer.Alarm(AlarmHandler.handler, us=INTERVAL, periodic=True)
