import pyray as rl
from ship import Ship

SCREEN_W = 800
SCREEN_H = 600

def main():
    rl.init_window(SCREEN_W, SCREEN_H, "statek")
    rl.set_target_fps(60)

    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        ship.update(dt)

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        ship.draw()

        rl.end_drawing()

    rl.close_window()

if __name__ == "__main__":
    main()