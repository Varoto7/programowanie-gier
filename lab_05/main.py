import pyray as rl
import random
from config import SCREEN_W, SCREEN_H
from ship import Ship
from asteroid import Asteroid


def main():
    rl.init_window(SCREEN_W, SCREEN_H, "Artemis II")
    rl.set_target_fps(60)

    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)

    asteroids = []
    for _ in range(5):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        size = random.choice(["LARGE", "MEDIUM", "SMALL"])
        asteroids.append(Asteroid(x, y, size))

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        ship.update(dt)
        ship.wrap()

        for ast in asteroids:
            ast.update(dt)
            ast.wrap()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        ship.draw()
        for ast in asteroids:
            ast.draw()

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()