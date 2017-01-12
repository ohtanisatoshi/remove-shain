# -*- coding: utf8 -*-
from PIL import Image
import sys
import os
import numpy as np

BLACK_THRESHOLD = 130
RED_THRESHOLD = 255 * 0.5

def is_red(r, g, b):
    r_g = r - g
    r_b = r - b
    if r > RED_THRESHOLD and r_g >= 0 and r_b >= 0:
        if r_g > 5 or r_b > 5:
            return True
        else:
            return False
    else:
        return False

filename = sys.argv[1]
filename_body, filename_ext = os.path.splitext(filename)
remove_filename = "{}_just_removed{}".format(filename_body, filename_ext)
img = Image.open(filename)
img_rgb = img.convert('RGB')
img_gray = img.convert('L')

def is_red2(r, g, b):
    m = float((r + g + b)) / 3
    v = ((r - m)**2 + (g - m)**2 + (b - m)**2) / 3
    sd = np.sqrt(v)
    r_s = (r - m) / sd
    g_s = (g - m) / sd
    b_s = (b - m) / sd
    if r_s > 1.35 and (g_s < 0.0 or b_s < 0.0):
        return True
    else:
        return False

w = img.size[0]
h = img.size[1]

for y in range(h):
    for x in range(w):
        r, g, b = img_rgb.getpixel((x, y))
        if is_red(r, g, b):
            img_rgb.putpixel((x, y), (255, 255, 255))
            #m = float((r + g + b)) / 3
            #v = ((r - m)**2 + (g - m)**2 + (b - m)**2) / 3
            #sd = np.sqrt(v)
            #r_s = (r - m) / sd
            #g_s = (g - m) / sd
            #b_s = (b - m) / sd
            #print "**({}, {}), ({}, {}, {}), ({:.2f}, {:.2f}, {:.2f})".format(x, y, r, g, b, r_s, g_s, b_s)
            #img_rgb.putpixel((x, y), (255, 255, 255))
        else:
            img_rgb.putpixel((x, y), (r, g, b))
            #img_rgb.putpixel((x, y), (255, 255, 255))

img_rgb.show()
img_rgb.save(remove_filename)
