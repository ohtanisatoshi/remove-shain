from PIL import Image


def is_red(r, g, b):
    r_g = r - g
    r_b = r - b
    if r_g > 0 and r_b > 0:
        if r_g > 5 or r_b > 5:
            return True
        else:
            return False
    else:
        return False

img = Image.open("receipt.jpg")
img_rgb = img.convert('RGB')
img_gray = img.convert('L')
#img_gray.show()

w = img.size[0]
h = img.size[1]

is_changed = True
while(is_changed):
    is_changed = False
    for wy in range(h-2):
        y = wy + 1
        for wx in range(w-2):
            x = wx + 1
            r, g, b = img_rgb.getpixel((x, y))
            if is_red(r, g, b):
                p_l_r, p_l_g, p_l_b = img_rgb.getpixel((x-1, y))
                p_r_r, p_r_g, p_r_b = img_rgb.getpixel((x+1, y))
                p_a_r, p_a_g, p_a_b = img_rgb.getpixel((x, y-1))
                p_b_r, p_b_g, p_b_b = img_rgb.getpixel((x, y+1))
                # 1: white, 2: red, 3: black
                c_l = 1
                if is_red(p_l_r, p_l_g, p_l_b):
                    c_l = 2
                else:
                    if img_gray.getpixel((x-1, y)) < 150:
                        c_l = 3
                c_r = 1
                if is_red(p_r_r, p_r_g, p_r_b):
                    c_r = 2
                else:
                    if img_gray.getpixel((x+1, y)) < 150:
                        c_r = 3
                c_a = 1
                if is_red(p_a_r, p_a_g, p_a_b):
                    c_a = 2
                else:
                    if img_gray.getpixel((x, y-1)) < 150:
                        c_a = 3
                c_b = 1
                if is_red(p_b_r, p_b_g, p_b_b):
                    c_b = 2
                else:
                    if img_gray.getpixel((x, y+1)) < 150:
                        c_b = 3
                if c_l == 3 or c_r == 3 or c_a == 3 or c_b == 3:
                    img_rgb.putpixel((x, y), (0, 0, 0))
                    is_changed = True
                else:
                    if c_l == 2 and c_r == 2 and c_a == 2 and c_b ==2:
                        img_rgb.putpixel((x, y), (r, g, b))
                    else:
                        img_rgb.putpixel((x, y), (255, 255, 255))
                        is_changed = True

                print "({}, {}), ({}, {}, {})".format(x, y, r, g, b)
                #img_rgb.putpixel((x, y), (255, 255, 255))
            else:
                img_rgb.putpixel((x, y), (r, g, b))

img_rgb.show()
img_rgb.save("removed.jpg")
