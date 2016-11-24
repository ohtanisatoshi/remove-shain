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


img = Image.open("seikyuusho.jpg")
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
                gray_l = 0
                c_l = 1
                if is_red(p_l_r, p_l_g, p_l_b):
                    c_l = 2
                else:
                    gray_l = img_gray.getpixel((x-1, y))
                    if gray_l < BLACK_THRESHOLD:
                        c_l = 3
                gray_r = 0
                c_r = 1
                if is_red(p_r_r, p_r_g, p_r_b):
                    c_r = 2
                else:
                    gray_r = img_gray.getpixel((x+1, y))
                    if gray_r < BLACK_THRESHOLD:
                        c_r = 3
                gray_a = 0
                c_a = 1
                if is_red(p_a_r, p_a_g, p_a_b):
                    c_a = 2
                else:
                    gray_a = img_gray.getpixel((x, y-1))
                    if gray_a < BLACK_THRESHOLD:
                        c_a = 3
                gray_b = 0
                c_b = 1
                if is_red(p_b_r, p_b_g, p_b_b):
                    c_b = 2
                else:
                    gray_b = img_gray.getpixel((x, y+1))
                    if gray_b < BLACK_THRESHOLD:
                        c_b = 3
                if c_l == 3 or c_r == 3 or c_a == 3 or c_b == 3:
                    r_total = 0
                    g_total = 0
                    b_total = 0
                    gray_p_count = 0
                    if c_l == 3:
                        gray_p_count += 1
                        r_total += p_l_r
                        g_total += p_l_g
                        b_total += p_l_b
                    if c_r == 3:
                        gray_p_count += 1
                        r_total += p_r_r
                        g_total += p_r_g
                        b_total += p_r_b
                    if c_a == 3:
                        gray_p_count += 1
                        r_total += p_a_r
                        g_total += p_a_g
                        b_total += p_a_b
                    if c_b == 3:
                        gray_p_count += 1
                        r_total += p_b_r
                        g_total += p_b_g
                        b_total += p_b_b

                    r_new_value = r_total/gray_p_count
                    g_new_value = g_total/gray_p_count
                    b_new_value = b_total/gray_p_count
                    if is_red(r_new_value, g_new_value, b_new_value):
                        if g_new_value < b_new_value:
                            r_new_value = g_new_value
                        else:
                            r_new_value = b_new_value

                    r_max = 0
                    g_max = 0
                    b_max = 0
                    gray_max = 0
                    if c_l == 3:
                        if gray_l < gray_max:
                            r_max = p_l_r
                            g_max = p_l_g
                            b_max = p_l_b
                    if c_r == 3:
                        if gray_r < gray_max:
                            r_max = p_r_r
                            g_max = p_r_g
                            b_max = p_r_b
                    if c_a == 3:
                        if gray_a < gray_max:
                            r_max = p_a_r
                            g_max = p_a_g
                            b_max = p_a_b
                    if c_b == 3:
                        if gray_b < gray_max:
                            r_max = p_b_r
                            g_max = p_b_g
                            b_max = p_b_b

                    #img_rgb.putpixel((x, y), (r_new_value, g_new_value, b_new_value))
                    img_rgb.putpixel((x, y), (r_max, g_max, b_max))
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
