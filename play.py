import time
import keyboard
import arrow
from PIL import ImageGrab

start_stop_key = "~"
press_release_sleep_ms = 10
loop_sleep_ms = 20


def press_release(key):
    keyboard.press(key)
    time.sleep(press_release_sleep_ms / 1000)
    keyboard.release(key)


def get_bounding_box(pixels, spacing=100):
    left_x = min(pixels, key=lambda x: x[0])[0] - spacing
    right_x = max(pixels, key=lambda x: x[0])[0] + spacing
    top_y = min(pixels, key=lambda y: y[1])[1] - spacing
    bottom_y = max(pixels, key=lambda y: y[1])[1] + spacing
    bbox = (left_x, top_y, right_x, bottom_y)
    print("bounding box {bbox}", bbox)
    return bbox


press_key = {
    arrow.RIGHT: lambda: press_release("right arrow"),
    arrow.UP: lambda: press_release("up arrow"),
    arrow.DOWN: lambda: press_release("down arrow"),
    arrow.LEFT: lambda: press_release("left arrow")
}

print_key = {
    arrow.RIGHT: lambda: print("   →"),
    arrow.UP: lambda: print("  ↑"),
    arrow.DOWN: lambda: print(" ↓"),
    arrow.LEFT: lambda: print("←")
}

if __name__ == "__main__":
    print("Press {} to start/stop".format(start_stop_key))

    while True:
        keyboard.wait(start_stop_key)

        arrow_xy = arrow.search(ImageGrab.grab())
        if arrow_xy is None:
            print("Arrow search could not find the player's arrows")
            continue

        bounding_box = get_bounding_box(arrow_xy.values())

        while not keyboard.is_pressed(start_stop_key):
            img = ImageGrab.grab(bbox=bounding_box)
            for arrow_id, xy in arrow_xy.items():
                x, y = xy
                rgb = img.getpixel((x - bounding_box[0], y - bounding_box[1]))
                if arrow.is_active(rgb):
                    press_key[arrow_id]()
                    print_key[arrow_id]()
                    time.sleep(loop_sleep_ms / 1000)

        print("Stopping")

    print("Exiting...")
