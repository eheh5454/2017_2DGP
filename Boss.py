from pico2d import *
import random


class AlienBoss:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 7

    image = None

    def __init__(self):
        self.x, self.y = random.randint(0, 200), random.randint(0, 100)
        self.frame = 0
        self.total_frames = 0
        if AlienBoss.image is None:
           AlienBoss.image = load_image('AlienBoss2.png')
        self.hp = 500
        self.xrunspeed = self.RUN_SPEED_PPS
        self.yrunspeed = random.choice([-1, 1]) * self.RUN_SPEED_PPS
        self.power = 15
        self.dir = 0

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += self.xrunspeed * frame_time
        self.y += self.yrunspeed * frame_time
        if self.x > 800:
            self.xrunspeed = -self.xrunspeed
            self.dir = 1
        if self.x < 0:
            self.xrunspeed = -self.xrunspeed
            self.dir = 0
        if self.y > 600:
            self.yrunspeed = -self.yrunspeed
        if self.y < 0:
            self.yrunspeed = -self.yrunspeed

    def draw(self):
        self.image.clip_draw(self.frame*200, self.dir*150, 200, 150, self.x, self.y)

    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 75, self.y + 75

    def draw_bb(self):
        draw_rectangle(*self.get_bb())