import pyray as rl
import math
from config import SCREEN_W, SCREEN_H, BULLET_SPEED, BULLET_TTL, BULLET_RADIUS


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL
        self.alive = True

        dir_x = math.sin(angle)
        dir_y = -math.cos(angle)

        self.vx = dir_x * BULLET_SPEED
        self.vy = dir_y * BULLET_SPEED

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.x = self.x % SCREEN_W
        self.y = self.y % SCREEN_H

        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

    def draw(self):
        rl.draw_circle(int(self.x), int(self.y), self.radius, rl.YELLOW)