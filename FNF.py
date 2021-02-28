import time
import random
import keyboard
import colorsys
from PIL import Image, ImageGrab

start_stop_key = "~"
arrow_color = (135, 163, 173)
RIGHT = 0
UP = 1
DOWN = 2
LEFT = 3


def color_check(pixel_color, target_color, error=10):
    (r1, g1, b1) = pixel_color
    (r2, g2, b2) = target_color
    c1 = r2 - error <= r1 <= r2 + error
    c2 = g2 - error <= g1 <= g2 + error
    c3 = b2 - error <= b1 <= b2 + error
    return c1 and c2 and c3


def is_grey(rgb):
    r, g, b = [x/255.0 for x in rgb]
    _, _, s = colorsys.rgb_to_hls(r, g, b)
    return s < .2


def arrow_search():
    black_color = (0, 0, 0)

    img = ImageGrab.grab()

    ARROWS = 8
    arrow_row = []
    arrow_max = {}  # Key=arrow, Value=max row
    arrow_px = {}  # Key=arrow, Value=last seen arrow_color pixel for given arrow

    # COLUMN SEARCH
    for row in range(img.height - 1, 0, -1):
        arrow_seen = False
        arrow = 0
        m = 0
        for col in range(img.width - 1, 0, -1):
            xy = (col, row)
            px = img.getpixel(xy)
            if color_check(px, black_color) and arrow_seen:
                # End of arrow
                img.putpixel(xy, (255, 0, 0))
                arrow += 1
                arrow_seen = False
                m = 0
                if arrow == ARROWS:
                    arrow_row.append(row)
            elif color_check(px, arrow_color):
                img.putpixel(xy, (0, 255, 0))
                arrow_seen = True
                m += 1
                if m > arrow_max.get(arrow, 0):
                    arrow_px[arrow] = xy
                    arrow_max[arrow] = m

    arrow_xy = dict((k, arrow_px[k]) for k in [RIGHT, UP, DOWN, LEFT] if k in arrow_px)

    # ==== DEBUG ====
    print(arrow_xy)
    for arrow, xy in arrow_xy.items():
        a, color = 5, (255, 0, 255)
        img.putpixel(xy, color)
        (x, y) = xy

        x += 50
        arrow_xy[arrow] = (x, y)

        for i in range(x, x - a, -1):
            img.putpixel((i, y), color)
        for i in range(x, x + a):
            img.putpixel((i, y), color)
        for j in range(y, y - a, -1):
            img.putpixel((x, j), color)
        for j in range(y, y + a):
            img.putpixel((x, j), color)
    img.save("debug.png")
    # ===============

    print("Search done")
    return arrow_xy


print("Press {} to start/stop".format(start_stop_key))

while True:
    keyboard.wait(start_stop_key)

    arrow_xy = arrow_search()

    press_release_sleep = 0.02

    if len(arrow_xy) == 4:
        while not keyboard.is_pressed(start_stop_key):
            img = ImageGrab.grab()
            for arrow, xy in arrow_xy.items():
                px = img.getpixel(xy)
                if not is_grey(px):
                    if arrow == RIGHT:
                        keyboard.press("right arrow")
                        time.sleep(press_release_sleep)
                        keyboard.release("right arrow")
                        print("right")
                    if arrow == UP:
                        keyboard.press("up arrow")
                        time.sleep(press_release_sleep)
                        keyboard.release("up arrow")
                        print("up")
                    if arrow == DOWN:
                        keyboard.press("down arrow")
                        time.sleep(press_release_sleep)
                        keyboard.release("down arrow")
                        print("down")
                    if arrow == LEFT:
                        keyboard.press("left arrow")
                        time.sleep(press_release_sleep)
                        keyboard.release("left arrow")
                        print("left")
            time.sleep(0.02)
    else:
        print("Error")

    print("Stopping")

print("Exiting...")
