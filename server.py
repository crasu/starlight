import machine
import socket
import re

PINS=["P" + str(i) for i in range(0, 13)]

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

PWM_CHANNEL = 0
pwm = machine.PWM(PWM_CHANNEL, frequency=5000)

print('listening on', addr)

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


while True:
    c, addr = s.accept()
    print('client connected from', addr)
    req = c.readline()
    process_header(c)

    (method, url) = parse_request(req)
    print("req: {} url: {}".format(method, url))

    if method == 'GET':
        (pin, level) = parse_url(url)
        if pin in PINS:
            pwm_c = pwm.channel(PWM_CHANNEL, pin=pin, duty_cycle=float(level)/100)
            print("Pin {} set to level {}".format(pin, level))
            c.send("HTTP/1.0 200 OK\n\nPin {} set to level {}\n\n".format(pin, level))
        else:
            c.send("HTTP/1.0 200 OK\n\nPin \"{}\" unknown\n".format(pin, level))
            

    else:
        c.send("HTTP/1.0 200 OK\n\nNo pin set\n")

    c.close()
