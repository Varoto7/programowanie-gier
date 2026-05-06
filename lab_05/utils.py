from config import SCREEN_W, SCREEN_H

def ghost_positions(x, y, size):
    """
    Zwraca listę pozycji (x, y) do narysowania w przypadku bliskości krawędzi.
    Zapewnia efekt widoczności po obu stronach przy przekraczaniu granicy ekranu.
    """
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