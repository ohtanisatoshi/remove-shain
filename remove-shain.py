# -*- coding: utf8 -*-
from PIL import Image

BLACK_THRESHOLD = 60

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
img_new = img.copy()
img_gray_data = img.convert('L').getdata()
#img_gray.show()

w = img.size[0]
h = img.size[1]

is_changed = True
while(is_changed):
    is_changed = False
    img_data = img_new.getdata()
    for wy in range(h-2):
        y = wy + 1
        for wx in range(w-2):
            x = wx + 1
            r, g, b = img_data[x+y*w]
            if is_red(r, g, b):
                is_changed = True

                p_l_r, p_l_g, p_l_b = img_data[(x-1) + y*w]
                p_r_r, p_r_g, p_r_b = img_data[(x+1) + y*w]
                p_a_r, p_a_g, p_a_b = img_data[(x) + (y-1)*w]
                p_b_r, p_b_g, p_b_b = img_data[(x)*w  + (y+1)*w]
                # 1: white, 2: red, 3: black
                gray_l = 0
                c_l = 1
                if is_red(p_l_r, p_l_g, p_l_b):
                    c_l = 2
                else:
                    gray_l = img_gray_data[(x-1) + y*w]
                    if gray_l < BLACK_THRESHOLD:
                        c_l = 3
                gray_r = 0
                c_r = 1
                if is_red(p_r_r, p_r_g, p_r_b):
                    c_r = 2
                else:
                    gray_r = img_gray_data[(x+1) + y*w]
                    if gray_r < BLACK_THRESHOLD:
                        c_r = 3
                gray_a = 0
                c_a = 1
                if is_red(p_a_r, p_a_g, p_a_b):
                    c_a = 2
                else:
                    gray_a = img_gray_data[x + (y-1)*w]
                    if gray_a < BLACK_THRESHOLD:
                        c_a = 3
                gray_b = 0
                c_b = 1
                if is_red(p_b_r, p_b_g, p_b_b):
                    c_b = 2
                else:
                    gray_b = img_gray_data[x + (y+1)*w]
                    if gray_b < BLACK_THRESHOLD:
                        c_b = 3
                # 周りにひとつでも黒があれば中心を黒に変換
                if c_l == 3 or c_r == 3 or c_a == 3 or c_b == 3:
                    black_p_count = 0
                    black_p_total_value = 0
                    if c_l == 3:
                        black_p_total_value += gray_l
                        black_p_count += 1
                    if c_r == 3:
                        black_p_total_value += gray_r
                        black_p_count += 1
                    if c_a == 3:
                        black_p_total_value += gray_a
                        black_p_count += 1
                    if c_b == 3:
                        black_p_total_value += gray_b
                        black_p_count += 1

                    black_p_average = black_p_total_value / black_p_count
                    #img_rgb.putpixel((x, y), (r_max, g_max, b_max))
                    img_new.putpixel((x, y), (black_p_average, black_p_average, black_p_average))
                else:
                    # 周りに黒がない場合
                    # 周りがすべて赤なら赤のままにしておく
                    if c_l == 2 and c_r == 2 and c_a == 2 and c_b ==2:
                        img_new.putpixel((x, y), (r, g, b))
                    else:
                        # 黒がない and すべて赤でない
                        # 白に変換
                        img_new.putpixel((x, y), (255, 255, 255))

                print "({}, {}), ({}, {}, {})".format(x, y, r, g, b)
                #img_rgb.putpixel((x, y), (255, 255, 255))
            else:
                img_new.putpixel((x, y), (r, g, b))

img_new.show()
img_new.save("removed.jpg")
