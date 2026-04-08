import pyray as rl
import math
import random
from config import ASTEROID_SIZES, SCREEN_W, SCREEN_H
from utils import ghost_positions

class Asteroid:
    def __init__(self, x, y, size_variant="MEDIUM"):
        self.x = x
        self.y = y
        self.alive = True # Nowa flaga

        params = ASTEROID_SIZES[size_variant]
        self.radius = params["radius"]

        speed = random.uniform(params["speed_min"], params["speed_max"])
        angle = random.uniform(0, math.tau)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.angle = 0.0
        self.rot_speed = random.uniform(-2.0, 2.0)

        self.verts = []
        num_points = params["points"]
        for i in range(num_points):
            a = (i / num_points) * math.tau
            r_offset = random.uniform(self.radius * 0.7, self.radius * 1.3)
            vx = math.cos(a) * r_offset
            vy = math.sin(a) * r_offset
            self.verts.append((vx, vy))

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.rot_speed * dt

    def wrap(self):
        self.x = self.x % SCREEN_W
        self.y = self.y % SCREEN_H

    def rotate_point(self, px, py, angle):
        nx = px * math.cos(angle) - py * math.sin(angle)
        ny = px * math.sin(angle) + py * math.cos(angle)
        return nx, ny

    def draw(self):
        positions = ghost_positions(self.x, self.y, self.radius)

        for px, py in positions:
            v_screen = []
            for vx, vy in self.verts:
                rx, ry = self.rotate_point(vx, vy, self.angle)
                v_screen.append(rl.Vector2(px + rx, py + ry))

            for i in range(len(v_screen)):
                p1 = v_screen[i]
                p2 = v_screen[(i + 1) % len(v_screen)]
                rl.draw_line_v(p1, p2, rl.WHITE)