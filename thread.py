import machine
import _thread

class Pwm:
    i=0
    enable=True
    p9_out = machine.Pin('P9', mode=machine.Pin.OUT)
    
    def __init__(self):
        pass

    @classmethod
    def run(cls):
        while cls.enable:
            cls.i=cls.i+1
            cls.p9_out(True)
            if cls.i % 10 == 0:
                cls.p9_out(False)

        print("terminating")

    @classmethod
    def stop(cls):
        cls.enable = False

def start():
    _thread.start_new_thread(Pwm.run, ())
