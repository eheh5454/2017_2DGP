from pico2d import *
import random

class Eye_monster:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = random.randint(0, 400), random.randint(0, 300)
        self.frame = 0
        self.image = load_image('Eye_monster.png')
        self.hp = 20
        self.xrunspeed = self.RUN_SPEED_PPS
        self.yrunspeed = self.RUN_SPEED_PPS

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 7
        self.x += self.xrunspeed * frame_time
        self.y += self.yrunspeed * frame_time
        if self.x > 800:
            self.xrunspeed = -self.xrunspeed
        if self.x < 0:
            self.xrunspeed = -self.xrunspeed
        if self.y > 600:
            self.yrunspeed = -self.yrunspeed
        if self.y < 0:
            self.yrunspeed = -self.yrunspeed

    def draw(self):
        self.image.clip_draw(self.frame*70, 0, 70, 70, self.x, self.y)

class Plant_monster:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = random.randint(400, 800), random.randint(0, 300)
        self.frame = 0
        self.image = load_image('Plant_monster.png')
        self.hp = 40
        self.xrunspeed = -self.RUN_SPEED_PPS
        self.yrunspeed = self.RUN_SPEED_PPS

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 4
        self.x += self.xrunspeed * frame_time
        self.y += self.yrunspeed * frame_time
        if self.x > 800:
            self.xrunspeed = -self.xrunspeed
        if self.x < 0:
            self.xrunspeed = -self.xrunspeed
        if self.y > 600:
            self.yrunspeed = -self.yrunspeed
        if self.y < 0:
            self.yrunspeed = -self.yrunspeed

    def draw(self):
        self.image.clip_draw(self.frame * 130, 0, 130, 150, self.x, self.y)

