from pico2d import *
import random


# eye_monster의 크기 = 70x70 픽셀, 140cm x 140cm
class Eyemonster:
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
        self.x, self.y = random.randint(0, 100), random.randint(0, 100)
        self.frame = 0
        self.total_frames = 0
        if Eyemonster.image is None:
           Eyemonster.image = load_image('Eyemonster.png')
        self.hp = 20
        self.xrunspeed = self.RUN_SPEED_PPS
        self.yrunspeed = random.choice([-1, 1]) * self.RUN_SPEED_PPS
        self.power = 5

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 7
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

    def get_bb(self):
        return self.x - 35, self.y - 35, self.x + 35, self.y + 35

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


# plant_monster의 크기 = 130 x 150픽셀, 260cm x 300cm
class Plantmonster:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    image = None

    def __init__(self):
        self.x, self.y = random.randint(700, 800), random.randint(0, 100)
        self.frame = 0
        self.total_frames = 0
        if Plantmonster.image is None:
            self.image = load_image('Plantmonster.png')
        self.hp = 40
        self.xrunspeed = -self.RUN_SPEED_PPS
        self.yrunspeed = random.choice([-1, 1]) * self.RUN_SPEED_PPS
        self.power = 10

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
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

    def get_bb(self):
        return self.x -65, self.y - 75, self.x + 65, self.y + 75

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


# power_monster의 크기 = 80 x 100 픽셀, 160cm x 200cm
class Powermonster:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x, self.y = random.randint(0, 100), random.randint(500, 600)
        self.frame = 0
        self.total_frames = 0
        if Powermonster.image is None:
           Powermonster.image = load_image('Powermonster.png')
        self.hp = 30
        self.xrunspeed = self.RUN_SPEED_PPS
        self.yrunspeed = random.choice([-1, 1]) * self.RUN_SPEED_PPS
        self.power = 10

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
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
        self.image.clip_draw(self.frame * 80, 0, 80, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 40, self.y + 50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


# 80 x 90 픽셀, 160cm x 180cm
class Swagemonster:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    image = None

    def __init__(self):
        self.x, self.y = random.randint(700, 800), random.randint(500, 600)
        self.frame = 0
        self.total_frames = 0
        if Swagemonster.image is None:
            self.image = load_image('Swagemonster.png')
        self.hp = 30
        self.xrunspeed = random.choice([-1, 1]) * self.RUN_SPEED_PPS
        self.yrunspeed = -self.RUN_SPEED_PPS
        self.power = 10

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
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
        self.image.clip_draw(self.frame * 80, 0, 80, 90, self.x, self.y)

    def get_bb(self):
        return self.x -40, self.y - 45, self.x + 40, self.y + 45

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Deleted_Eyemonster:
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    def __init__(self):
        self.image = load_image("deleted_em.png")
        self.frame = 0
        self.total_frames = 0
        self.x, self.y = 0, 0

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 70, 0, 70, 70, self.x, self.y)


class Deleted_Powermonster:
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    def __init__(self):
        self.image = load_image("deleted_pm.png")
        self.frame = 0
        self.total_frames = 0
        self.x, self.y = 0, 0

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 100, self.x, self.y)


class Deleted_Plantmonster:
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    def __init__(self):
        self.image = load_image("deleted_plm.png")
        self.frame = 0
        self.total_frames = 0
        self.x, self.y = 0, 0

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 130, 0, 130, 130, self.x, self.y)


class Deleted_Swagemonster:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    def __init__(self):
        self.image = load_image("deleted_sm.png")
        self.frame = 0
        self.total_frames = 0
        self.x, self.y = 0, 0

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 90, self.x, self.y)
