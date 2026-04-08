import pyray as rl
import math
from config import ROT_SPEED, THRUST, FRICTION, MAX_SPEED, DEBUG, SCREEN_W, SCREEN_H
from utils import ghost_positions

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.0
        self.radius = 15.0
        self.verts = [(0, -15), (-10, 10), (10, 10)]
        self.is_thrusting = False

    def rotate_point(self, px, py, angle):
        nx = px * math.cos(angle) - py * math.sin(angle)
        ny = px * math.sin(angle) + py * math.cos(angle)
        return nx, ny

    def get_nose_position(self):
        nx, ny = self.rotate_point(0, -15, self.angle)
        return self.x + nx, self.y + ny

    def reset(self):
        self.x = SCREEN_W / 2
        self.y = SCREEN_H / 2
        self.vx = 0.0
        self.vy = 0.0

    def update(self, dt):
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.angle += ROT_SPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.angle -= ROT_SPEED * dt

        self.is_thrusting = rl.is_key_down(rl.KeyboardKey.KEY_UP)
        if self.is_thrusting:
            dir_x = math.sin(self.angle)
            dir_y = -math.cos(self.angle)

            self.vx += dir_x * THRUST * dt
            self.vy += dir_y * THRUST * dt

        if rl.is_key_down(rl.KeyboardKey.KEY_Z):
            self.vx *= max(0.0, 1.0 - 5.0 * dt)
            self.vy *= max(0.0, 1.0 - 5.0 * dt)

        speed = math.hypot(self.vx, self.vy)

        if speed > 0:
            new_speed = speed - (FRICTION * dt)
            if new_speed < 0:
                new_speed = 0

            if new_speed > MAX_SPEED:
                new_speed = MAX_SPEED

            self.vx = (self.vx / speed) * new_speed
            self.vy = (self.vy / speed) * new_speed

        self.x += self.vx * dt
        self.y += self.vy * dt

    def wrap(self):
        self.x = self.x % SCREEN_W
        self.y = self.y % SCREEN_H

    def draw(self):
        positions = ghost_positions(self.x, self.y, self.radius)

        for px, py in positions:
            v_screen = []
            for vx, vy in self.verts:
                rx, ry = self.rotate_point(vx, vy, self.angle)
                v_screen.append(rl.Vector2(px + rx, py + ry))

            rl.draw_triangle_lines(v_screen[0], v_screen[1], v_screen[2], rl.RAYWHITE)

            if self.is_thrusting:
                p_screen = []
                for vx, vy in [(0, 25), (-5, 12), (5, 12)]:
                    rx, ry = self.rotate_point(vx, vy, self.angle)
                    p_screen.append(rl.Vector2(px + rx, py + ry))
                rl.draw_triangle_lines(p_screen[0], p_screen[2], p_screen[1], rl.ORANGE)

        if DEBUG:
            rl.draw_line(int(self.x), int(self.y), int(self.x + self.vx), int(self.y + self.vy), rl.GREEN)
            speed_val = math.hypot(self.vx, self.vy)
            rl.draw_text(f"Speed: {speed_val:.1f}", 10, 10, 20, rl.GRAY)
            rl.draw_text(f"FPS: {rl.get_fps()}", 10, 35, 20, rl.GRAY)