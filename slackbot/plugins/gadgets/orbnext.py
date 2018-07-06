from collections import OrderedDict
from random import randint
from will import settings
from time import sleep
import urllib.request, urllib.error, urllib.parse
import logging
import json
import sys

DEVICE_ID = getattr(settings, 'ORBNEXT_DEVICE_ID', None)

URL = 'https://agent.electricimp.com/{}'.format(DEVICE_ID)

colors = OrderedDict()
colors['off'] = '000000'
colors['red'] = 'FF0000'
colors['orange'] = 'FF3000'
colors['yellow'] = 'FFFF00'
colors['green'] = '00FF00'
colors['blue'] = '0000FF'
colors['indigo'] = '220077'
colors['violet'] = '440066'
colors['cyan'] = '00FFFF'
colors['pink'] = 'FF00FF'
colors['white'] = 'FFFFFF'

def set_color(color):
    if color not in colors:
        return False
    data = {"program":"Demo","color":"#{}".format(colors.get(color))}
    payload = bytes(json.dumps(data), 'utf-8')
    req = urllib.request.Request(URL, payload)
    response = urllib.request.urlopen(req)
    resp_data = response.read()
    return resp_data == b'Color Demo Request Received'

def disco():
    while True:
        r, g, b = [randint(0,255) for x in range(0,3)]
        color = '{:02x}{:02x}{:02x}'.format(r,g,b)
        set_color(color)
        sleep(.5)

def rainbow():
    for color in ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'off'):
        set_color(colors[color])
        sleep(1)

def pulsate(color):
    valid_colors = ('red', 'yellow', 'green', 'blue', 'cyan', 'pink', 'white')

    if color not in valid_colors:
        return

    colorstring = colors[color].replace('FF', '{:02x}')
    num_colors = colors[color].count('FF')

    def pulse(value):
        pulse_colors = [x for _ in range(0, num_colors)]
        set_color(colorstring.format(*pulse_colors))

    while True:
        for x in range(0,255,31):
            pulse(x)
        for x in range(255,0,-31):
            pulse(x)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        color = sys.argv[1]
        if color in colors:
            print(('Setting color {}, code {}'.format(color, colors[color])))
            set_color(colors[color])
        elif color == 'disco':
            disco()
        elif color == 'rainbow':
            rainbow()
        else:
            print('Color {} not defined.')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'pulsate':
            pulsate(sys.argv[2])

        sys.exit()
