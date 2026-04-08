import pyray as rl
import random
from config import SCREEN_W, SCREEN_H, MAX_BULLETS
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import check_collision_circles


def main():
    rl.init_window(SCREEN_W, SCREEN_H, "Artemis II")
    rl.set_target_fps(60)

    rl.init_audio_device()
    snd_shoot = rl.load_sound("assets/shoot.wav")
    snd_explode = rl.load_sound("assets/explode.wav")
    tex_stars = rl.load_texture("assets/stars.png")

    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)

    asteroids = []
    for _ in range(5):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        size = random.choice(["LARGE", "MEDIUM", "SMALL"])
        asteroids.append(Asteroid(x, y, size))

    bullets = []
    explosions = []

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        ship.update(dt)
        ship.wrap()

        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            if len(bullets) < MAX_BULLETS:
                nx, ny = ship.get_nose_position()
                bullets.append(Bullet(nx, ny, ship.angle))
                rl.play_sound(snd_shoot)

        for b in bullets:
            b.update(dt)

        for ast in asteroids:
            ast.update(dt)
            ast.wrap()

        for exp in explosions:
            exp.update(dt)

        for b in bullets:
            if not b.alive: continue
            for ast in asteroids:
                if not ast.alive: continue

                if check_collision_circles(b.x, b.y, b.radius, ast.x, ast.y, ast.radius):
                    b.alive = False
                    ast.alive = False
                    explosions.append(Explosion(ast.x, ast.y, ast.radius * 2))
                    rl.play_sound(snd_explode)

        for ast in asteroids:
            if not ast.alive: continue
            if check_collision_circles(ship.x, ship.y, ship.radius, ast.x, ast.y, ast.radius):
                explosions.append(Explosion(ship.x, ship.y, ship.radius * 2))
                rl.play_sound(snd_explode)
                ship.reset()
                ast.alive = False

        bullets = [b for b in bullets if b.alive]
        asteroids = [ast for ast in asteroids if ast.alive]
        explosions = [exp for exp in explosions if exp.alive]

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.draw_texture(tex_stars, 0, 0, rl.WHITE)

        ship.draw()
        for b in bullets:
            b.draw()
        for ast in asteroids:
            ast.draw()
        for exp in explosions:
            exp.draw()

        rl.end_drawing()

    rl.unload_texture(tex_stars)
    rl.unload_sound(snd_shoot)
    rl.unload_sound(snd_explode)
    rl.close_audio_device()

    rl.close_window()


if __name__ == "__main__":
    main()