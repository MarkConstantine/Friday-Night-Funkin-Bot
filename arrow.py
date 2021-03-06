import colorsys
from PIL import Image

black_rgb = (0, 0, 0)
red_rgb = (255, 0, 0)
green_rgb = (0, 255, 0)
blue_rgb = (0, 0, 255)
arrow_rgb = (135, 163, 173)
# arrow_color_main = (135, 163, 173)
# arrow_color_week6 = (162, 186, 200)
# black_color_main = (0, 0, 0)
# black_color_week6 = (64, 64, 71)
RIGHT, UP, DOWN, LEFT = 0, 1, 2, 3


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


def search(image):
    debug_image = image.copy()

    arrow_max = {}  # Key=arrow_id, Value=max row
    arrow_xy = {}  # Key=arrow_id, Value=last seen pixel coordinates for given arrow

    # COLUMN SEARCH - Find the left-most edge of each arrow
    for y in range(image.height - 1, 0, -1):
        arrow_seen = False
        arrow_id = 0
        row_max = 0
        # Loop backwards because player arrows are on the right
        for x in range(image.width - 1, 0, -1):
            xy = (x, y)
            rgb = image.getpixel(xy)
            if color_check(rgb, black_rgb) and arrow_seen:
                # End of arrow
                debug_image.putpixel(xy, red_rgb)
                arrow_id += 1
                arrow_seen = False
                row_max = 0
            elif color_check(rgb, arrow_rgb):
                debug_image.putpixel(xy, green_rgb)
                arrow_seen = True
                row_max += 1
                if row_max > arrow_max.get(arrow_id, 0):
                    arrow_xy[arrow_id] = xy
                    arrow_max[arrow_id] = row_max

    # First 4 pixels should be the pixel coordinates for each arrow of the player
    arrow_coordinates = dict((k, arrow_xy[k])
                             for k in [RIGHT, UP, DOWN, LEFT] if k in arrow_xy)

    # ROW SEARCH - Find the center of the arrow
    for arrow_id, xy in arrow_coordinates.items():
        (x, y) = xy
        largest_column = 0

        # Loop forwards in columns
        rgb = image.getpixel((x, y))
        while color_check(rgb, arrow_rgb):
            # Traverse ROW up
            up = y - 1
            rgb = image.getpixel((x, up))
            while up > 0 and color_check(rgb, arrow_rgb):
                rgb = image.getpixel((x, up))
                up -= 1

            # Traverse ROW down
            down = y + 1
            rgb = image.getpixel((x, down))
            while down < image.height and color_check(rgb, arrow_rgb):
                rgb = image.getpixel((x, down))
                down += 1

            # Save if taller column
            up_count, down_count = abs(up - y), abs(down - y)
            column_count = up_count + down_count
            if column_count > largest_column:
                largest_column = column_count
                arrow_coordinates[arrow_id] = (x, y)

            x += 1
            rgb = image.getpixel((x, y))

    # ==== DEBUG ====
    print(arrow_coordinates)
    for arrow_id, xy in arrow_coordinates.items():
        plus_size = 5
        color = blue_rgb
        (x, y) = xy

        # Draw plus onto debug_image to easily identify chosen arrow pixels
        debug_image.putpixel(xy, color)
        for i in range(x, x - plus_size, -1):
            debug_image.putpixel((i, y), color)
        for i in range(x, x + plus_size):
            debug_image.putpixel((i, y), color)
        for j in range(y, y - plus_size, -1):
            debug_image.putpixel((x, j), color)
        for j in range(y, y + plus_size):
            debug_image.putpixel((x, j), color)
    debug_image.save("debug.png")
    # ===============

    print("Search done")
    return arrow_coordinates if len(arrow_coordinates) == 4 else None
