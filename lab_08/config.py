SCREEN_W = 800
SCREEN_H = 600
TARGET_FPS = 60

ROT_SPEED = 3.5
THRUST = 250.0
FRICTION = 40.0
MAX_SPEED = 350.0
DEBUG = False

BULLET_SPEED = 600.0
BULLET_TTL = 1.5
BULLET_RADIUS = 3.0
MAX_BULLETS = 5

EXPLOSION_DURATION = 0.4

ASTEROID_PARAMS = {
    3: {"radius": 40, "speed_min": 20, "speed_max": 50, "points": 10, "verts": 10},
    2: {"radius": 20, "speed_min": 50, "speed_max": 100, "points": 20, "verts": 8},
    1: {"radius": 10, "speed_min": 100, "speed_max": 200, "points": 30, "verts": 6}
}