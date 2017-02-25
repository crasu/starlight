import time

def th_func(delay, id):
    while True:
        import time
        time.sleep(delay)
        print("Running thread {}".format(id))

_thread.start_new_thread(th_func, (1, "hello"))
