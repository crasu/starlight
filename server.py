import machine
import socket
import re

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
        print("Could not parse: {}".format(url))
        return ("", "")

def parse_url(url):
    m = re.match("/(P[0-9][0-9])/[0-9]+", url)
    if m:
        return (m.group(1), m.group(2))
    else:
        print("Could not parse: {}".format(url))
        return ("", "")

while True:
    c, addr = s.accept()
    print('client connected from', addr)
    req = c.readline()
    (method, url) = parse_request(req)
    print("req: {} url: {}".format(method, url))

    if method == 'GET':
        (pin, level) = parse_url(url)
        print("pin: {} level: {}".format(pin, level)
        pwm_c = pwm.channel(PWM_CHANNEL, pin='P12', duty_cycle=0.5)

    c.send("HTTP/1.0 200 OK\n\nOK!\n")
    c.close()
