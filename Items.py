from pico2d import *
import random




class Special_attack_item():
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    image = None

    def __init__(self):
        self.x, self.y = random.randint(0, 800), random.randint(0, 600)
        if Special_attack_item.image is None:
            Special_attack_item.image = load_image("special_attack_item.png")
        self.frame = 0
        self.total_frames = 0
        vector = [-1, 1]
        self.xrunspeed = random.choice(vector) * self.RUN_SPEED_PPS
        self.yrunspeed = random.choice(vector) * self.RUN_SPEED_PPS

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2
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
        self.image.clip_draw(self.frame * 40, 0, 40, 40, self.x, self.y)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20


class Bomb_item():
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    image = None

    def __init__(self):
        self.x, self.y = random.randint(0, 800), random.randint(0, 600)
        if Bomb_item.image is None:
            Bomb_item.image = load_image("bomb_item.png")
        self.frame = 0
        self.total_frames = 0
        vector = [-1, 1]
        self.xrunspeed = random.choice(vector) * self.RUN_SPEED_PPS
        self.yrunspeed = random.choice(vector) * self.RUN_SPEED_PPS

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2
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
        self.image.clip_draw(self.frame * 20, 0, 20, 20, self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10