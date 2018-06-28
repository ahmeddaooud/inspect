import re
import time
import random
import base64

from flask import session, request, render_template

from inspector.views import expand_recent_bins


def random_byte(gradient=None, floor=0):
    factor = gradient or 1
    max = int(255 / factor)
    return random.randint(floor, max) * factor

def solid16x16gif_datauri(r,g,b):
    return "data:image/gif;base64,R0lGODlhEAAQAIAA%sACH5BAQAAAAALAAAAAAQABAAAAIOhI+py+0Po5y02ouzPgUAOw==" \
        % base64.b64encode(bytearray([0,r,g,b,0,0]))

def random_color():
    return random_byte(10, 5), random_byte(10, 5), random_byte(10, 5)

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"): 
    return ((num == 0) and  "0" ) or (baseN(num // b, b).lstrip("0") + numerals[num % b])

def tinyid(size=6):
    merchantid = re.sub('[^A-Za-z0-9]+', '', request.form['name'])
    if merchantid == '':
        id = '%s%s' % (
            baseN(abs(hash(time.time())), 36),
            baseN(abs(hash(time.time())), 36))
        return id[0:8]
    else:
        id = merchantid
        return id[0:20]

