from pico2d import *
import random

alienbosstime = 0.0

class AlienBoss:
    RIGHT_RUN, LEFT_RUN, RIGHT_SPEED_RUN, LEFT_SPEED_RUN = 0, 1, 2, 3
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
        self.x, self.y = random.randint(100, 200), random.randint(100, 500)
        self.frame = 0
        self.total_frames = 0
        if AlienBoss.image is None:
           AlienBoss.image = load_image('AlienBoss3.png')
        self.hp = 700
        self.xrunspeed = self.RUN_SPEED_PPS
        self.yrunspeed = random.choice([-1, 1]) * self.RUN_SPEED_PPS
        self.power = 1
        self.state = self.RIGHT_RUN
        self.time = 0.0

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        if self.state in (self.RIGHT_SPEED_RUN, self.LEFT_SPEED_RUN):
            self.x += self.xrunspeed * frame_time * 2
            self.y += self.yrunspeed * frame_time * 2
        else:
            self.x += self.xrunspeed * frame_time
            self.y += self.yrunspeed * frame_time
        if self.x > 800:
            self.xrunspeed = -self.xrunspeed
            self.state = self.LEFT_RUN
        if self.x < 0:
            self.xrunspeed = -self.xrunspeed
            self.state = self.RIGHT_RUN
        if self.y > 600:
            self.yrunspeed = -self.yrunspeed
            self.state = self.RIGHT_SPEED_RUN
        if self.y < 0:
            self.yrunspeed = -self.yrunspeed
            self.state = self.LEFT_SPEED_RUN

    def draw(self):
        self.image.clip_draw(self.frame*300, self.state*200, 300, 200, self.x, self.y)

    def get_bb(self):
        return self.x - 150, self.y - 150, self.x + 100, self.y + 100

    def draw_bb(self):
        draw_rectangle(*self.get_bb())