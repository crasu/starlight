import machine
import socket
import re
import select
import utime
import machine
import pycom

PINS=["P" + str(i) for i in range(2, 13)]

outputs = { pin: machine.Pin(pin, mode=machine.Pin.OUT) for pin in PINS }
for output in outputs:
    output = False

pycom.heartbeat(False)

def parse_request(req):
    m = re.match("([^\s]+) ([^\s]+) HTTP/.*\r\n", req)
    if m:
        return (m.group(1), m.group(2))
    else:
        print("Could not parse: {}".format(req))
        return ("", "")

def parse_url(url):
    m = re.match("/(P[0-9]+)/([0-9]+)", url)
    if m:
        return (m.group(1), m.group(2))
    else:
        print("Could not parse: {}".format(url))
        return ("", "")

def process_header(c):
    while True:
        header = c.readline()
        if header == b"" or header == b"\r\n":
            break
        print("H:{}".format(header))

def create_socket():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.setblocking(0)
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)
    return s

def handle_http(s, levels):
    readable, writable, exceptional = select.select([s], [s], [s], 0)
    if len(readable) > 0:
        print("handling connection")
    else:
        return levels

    c, addr = s.accept()
    print('client connected from', addr)
    req = c.readline()
    process_header(c)

    (method, url) = parse_request(req)
    print("req: {} url: {}".format(method, url))

    if method == 'GET':
        (pin, level) = parse_url(url)
        if pin in PINS:
            levels[pin] = int(level)
            print("Pin {} set to level {}".format(pin, level))
            c.send("HTTP/1.0 200 OK\n\nPin {} set to level {}\n\n".format(pin, level))
        else:
            c.send("HTTP/1.0 200 OK\n\nPin \"{}\" unknown\n".format(pin, level))
    else:
        c.send("HTTP/1.0 200 OK\n\nNo pin set\n")

    c.close()
    return levels

def do_pwm(levels):
    for i in range(0, 1500):
        for pin in PINS:
            on = False
            level = levels[pin]

            if level <= 0 or level >= 100:
                on = level>= 100
            else:
                if level < 50:
                    on = i % (100//level) == 0
                else:
                    on = i % (100//(100-level)) != 0

            outputs[pin](on)

def start():
    s = create_socket()
    levels = { pin: 0 for pin in PINS }
    while True:
        levels = handle_http(s, levels)
        do_pwm(levels)
