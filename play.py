import time
import keyboard
import arrow
from PIL import ImageGrab

start_stop_key = "~"
press_release_sleep = 0.02
loop_sleep = 0.02


print("Press {} to start/stop".format(start_stop_key))

while True:
    keyboard.wait(start_stop_key)

    arrow_xy = arrow.search(ImageGrab.grab())
    if arrow_xy is None:
        print("Arrow search could not find the player's arrows")
        continue

    while not keyboard.is_pressed(start_stop_key):
        img = ImageGrab.grab()
        for a, xy in arrow_xy.items():
            px = img.getpixel(xy)
            if not arrow.is_grey(px):
                if a == arrow.RIGHT:
                    keyboard.press("right arrow")
                    time.sleep(press_release_sleep)
                    keyboard.release("right arrow")
                    print("right")
                if a == arrow.UP:
                    keyboard.press("up arrow")
                    time.sleep(press_release_sleep)
                    keyboard.release("up arrow")
                    print("up")
                if a == arrow.DOWN:
                    keyboard.press("down arrow")
                    time.sleep(press_release_sleep)
                    keyboard.release("down arrow")
                    print("down")
                if a == arrow.LEFT:
                    keyboard.press("left arrow")
                    time.sleep(press_release_sleep)
                    keyboard.release("left arrow")
                    print("left")
        time.sleep(loop_sleep)

    print("Stopping")

print("Exiting...")
