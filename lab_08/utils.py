import math
from config import SCREEN_W, SCREEN_H

def ghost_positions(x, y, size):
    positions = [(x, y)]

    wrap_x = None
    if x < size:
        wrap_x = x + SCREEN_W
    elif x > SCREEN_W - size:
        wrap_x = x - SCREEN_W

    wrap_y = None
    if y < size:
        wrap_y = y + SCREEN_H
    elif y > SCREEN_H - size:
        wrap_y = y - SCREEN_H

    if wrap_x is not None:
        positions.append((wrap_x, y))
    if wrap_y is not None:
        positions.append((x, wrap_y))
    if wrap_x is not None and wrap_y is not None:
        positions.append((wrap_x, wrap_y))

    return positions

def check_collision_circles(x1, y1, r1, x2, y2, r2):
    dist = math.hypot(x1 - x2, y1 - y2)
    return dist <= (r1 + r2)

def cleanup_dead(item_list):
    return [x for x in item_list if x.alive]