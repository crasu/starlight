# Installation #

    pip install ampy

# Upload to wipy #

    ~/.local/bin/ampy --port /dev/ttyUSB0 -b 115200 put <filename>
    cu -l /dev/ttyUSB0
    lftp -e 'set ftp:ssl-allow false' ftp://micro:python@IP

# Curl #
    curl http://192.168.100.120/P12/1
