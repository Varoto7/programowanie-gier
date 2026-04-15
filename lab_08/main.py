import pyray as rl
import random
import os
import math
from enum import Enum, auto

from config import SCREEN_W, SCREEN_H, MAX_BULLETS, TARGET_FPS
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import check_collision_circles, cleanup_dead


class State(Enum):
    MENU = auto()
    GAME = auto()
    GAME_OVER = auto()


state = State.MENU
score = 0
best = 0
wave = 1
victory = False

ship = None
asteroids = []
bullets = []
explosions = []
wave_cooldown = 0.0

snd_shoot = None
snd_explode = None
tex_stars = None


def load_high_score():
    global best
    try:
        if os.path.exists("scores.txt"):
            with open("scores.txt", "r") as f:
                best = int(f.read().strip())
    except Exception:
        best = 0


def save_high_score():
    global best
    try:
        with open("scores.txt", "w") as f:
            f.write(str(best))
    except Exception:
        pass


def spawn_wave():
    """Generuje nową falę asteroid, upewniając się, że nie spawnują się na statku"""
    global wave, asteroids
    count = 3 + wave  # Więcej asteroid z każdą falą

    # Współrzędne środka (gdzie spawnuje się statek)
    center_x = SCREEN_W / 2
    center_y = SCREEN_H / 2
    safe_radius = 100.0

    for _ in range(count):
        while True:
            x = random.uniform(0, SCREEN_W)
            y = random.uniform(0, SCREEN_H)

            dist = math.hypot(x - center_x, y - center_y)
            if dist > safe_radius:
                break

        asteroids.append(Asteroid(x, y, level=3))


def init_game(reset_score=True):
    global ship, asteroids, bullets, explosions, score, wave, victory, wave_cooldown

    ship = Ship(SCREEN_W / 2, SCREEN_H / 2)
    bullets.clear()
    explosions.clear()
    asteroids.clear()

    if reset_score:
        score = 0
        wave = 1

    victory = False
    wave_cooldown = 0.0
    spawn_wave()


def update_menu(dt):
    global state
    if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
        init_game(reset_score=True)
        state = State.GAME


def draw_menu():
    text = "ARTEMIS II"
    w = rl.measure_text(text, 40)
    rl.draw_text(text, int((SCREEN_W - w) / 2), 200, 40, rl.RAYWHITE)

    text_start = "PRESS ENTER TO START"
    w2 = rl.measure_text(text_start, 20)
    rl.draw_text(text_start, int((SCREEN_W - w2) / 2), 300, 20, rl.GRAY)


def update_game(dt):
    global state, score, victory, wave, asteroids, bullets, explosions, wave_cooldown

    if wave_cooldown > 0:
        wave_cooldown -= dt
        if wave_cooldown <= 0:
            spawn_wave()

    ship.update(dt)
    ship.wrap()

    if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
        if len(bullets) < MAX_BULLETS:
            nx, ny = ship.get_nose_position()
            bullets.append(Bullet(nx, ny, ship.angle))
            rl.play_sound(snd_shoot)

    for b in bullets: b.update(dt)
    for ast in asteroids:
        ast.update(dt)
        ast.wrap()
    for exp in explosions: exp.update(dt)

    new_asteroids = []

    for b in bullets:
        if not b.alive: continue
        for ast in asteroids:
            if not ast.alive: continue
            if check_collision_circles(b.x, b.y, b.radius, ast.x, ast.y, ast.radius):
                b.alive = False
                ast.alive = False
                score += ast.points
                explosions.append(Explosion(ast.x, ast.y, ast.radius * 2))
                rl.play_sound(snd_explode)
                new_asteroids.extend(ast.split())

    asteroids.extend(new_asteroids)

    for ast in asteroids:
        if not ast.alive: continue
        if check_collision_circles(ship.x, ship.y, ship.radius, ast.x, ast.y, ast.radius):
            explosions.append(Explosion(ship.x, ship.y, ship.radius * 2))
            rl.play_sound(snd_explode)
            ast.alive = False
            state = State.GAME_OVER

    bullets[:] = cleanup_dead(bullets)
    asteroids[:] = cleanup_dead(asteroids)
    explosions[:] = cleanup_dead(explosions)

    if len(asteroids) == 0 and wave_cooldown <= 0:
        if wave >= 3:
            victory = True
            state = State.GAME_OVER
        else:
            wave += 1
            wave_cooldown = 2.0


def draw_hud():
    rl.draw_text(f"SCORE: {score}", 10, 10, 20, rl.RAYWHITE)
    rl.draw_text(f"BEST: {best}", 10, 40, 20, rl.GOLD)
    if wave_cooldown > 0:
        rl.draw_text(f"WAVE {wave} INCOMING...", int(SCREEN_W / 2) - 100, 50, 20, rl.YELLOW)
    else:
        rl.draw_text(f"WAVE: {wave}/3", SCREEN_W - 120, 10, 20, rl.RAYWHITE)


def draw_game():
    if ship.alive: ship.draw()
    for b in bullets: b.draw()
    for ast in asteroids: ast.draw()
    for exp in explosions: exp.draw()
    draw_hud()


def update_gameover(dt):
    global state, best

    if score > best:
        best = score
        save_high_score()

    for exp in explosions:
        exp.update(dt)

    if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
        state = State.MENU


def draw_gameover():
    for ast in asteroids: ast.draw()
    for exp in explosions: exp.draw()

    msg = "VICTORY!" if victory else "GAME OVER"
    color = rl.GREEN if victory else rl.RED
    w = rl.measure_text(msg, 50)
    rl.draw_text(msg, int((SCREEN_W - w) / 2), 200, 50, color)

    score_msg = f"FINAL SCORE: {score}"
    w2 = rl.measure_text(score_msg, 30)
    rl.draw_text(score_msg, int((SCREEN_W - w2) / 2), 300, 30, rl.RAYWHITE)

    restart_msg = "PRESS ENTER TO RETURN TO MENU"
    w3 = rl.measure_text(restart_msg, 20)
    rl.draw_text(restart_msg, int((SCREEN_W - w3) / 2), 400, 20, rl.GRAY)


def main():
    global snd_shoot, snd_explode, tex_stars

    rl.init_window(SCREEN_W, SCREEN_H, "Artemis II")
    rl.set_target_fps(TARGET_FPS)

    rl.init_audio_device()
    snd_shoot = rl.load_sound("assets/shoot.wav")
    snd_explode = rl.load_sound("assets/explode.wav")
    tex_stars = rl.load_texture("assets/stars.jpg")

    load_high_score()

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        if state == State.MENU:
            update_menu(dt)
        elif state == State.GAME:
            update_game(dt)
        elif state == State.GAME_OVER:
            update_gameover(dt)

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_texture(tex_stars, 0, 0, rl.WHITE)

        if state == State.MENU:
            draw_menu()
        elif state == State.GAME:
            draw_game()
        elif state == State.GAME_OVER:
            draw_gameover()

        rl.end_drawing()

    save_high_score()

    rl.unload_texture(tex_stars)
    rl.unload_sound(snd_shoot)
    rl.unload_sound(snd_explode)
    rl.close_audio_device()
    rl.close_window()


if __name__ == "__main__":
    main()