import pyray as rl
from config import EXPLOSION_DURATION

class Explosion:
    def __init__(self, x, y, target_radius):
        self.x = x
        self.y = y
        self.target_radius = target_radius
        self.duration = EXPLOSION_DURATION
        self.timer = 0.0
        self.alive = True

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.alive = False

    def draw(self):
        if not self.alive: return

        progress = self.timer / self.duration
        current_radius = self.target_radius * progress

        alpha = int(255 * (1.0 - progress))
        color = rl.Color(255, 165, 0, alpha)

        rl.draw_circle_lines(int(self.x), int(self.y), current_radius, color)