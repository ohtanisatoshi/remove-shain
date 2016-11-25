# -*- coding: utf8 -*-
from PIL import Image

BLACK_THRESHOLD = 130

def is_red(r, g, b):
    r_g = r - g
    r_b = r - b
    if r_g >= 0 and r_b >= 0:
        if r_g > 5 or r_b > 5:
            return True
        else:
            return False
    else:
        return False


img = Image.open("Jobwise.jpg")
img_rgb = img.convert('RGB')
img_gray = img.convert('L')
#img_gray.show()

w = img.size[0]
h = img.size[1]

for y in range(h):
    for x in range(w):
        r, g, b = img_rgb.getpixel((x, y))
        if is_red(r, g, b):
            img_rgb.putpixel((x, y), (255, 255, 255))
            print "({}, {}), ({}, {}, {})".format(x, y, r, g, b)
            #img_rgb.putpixel((x, y), (255, 255, 255))
        else:
            img_rgb.putpixel((x, y), (r, g, b))

img_rgb.show()
img_rgb.save("just-removed.jpg")
