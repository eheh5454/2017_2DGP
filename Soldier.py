from pico2d import *
import random

space = None
soldier = None

UP = False
DOWN = False
RIGHT = False
LEFT = False

basic_attacks = []
missile_attacks = []

# soldier의 크기 = 50 x 80픽셀, 키 160cm
class Soldier:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.x, self.y = 400, 300
        self.dir = 0
        self.image = load_image('soldier.png')
        self.frame = 0
        self.hp = 50
        self.total_frames = 0

    def move(self):
        if UP:
          self.y += self.runspeed
        if DOWN:
          self.y -= self.runspeed
        if RIGHT:
          self.x += self.runspeed
          self.dir = 0
        if LEFT:
          self.x -= self.runspeed
          self.dir = 1

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME *frame_time
        self.frame = int(self.total_frames) % 6
        self.move()

    def draw(self):
        self.image.clip_draw(self.frame*50, self.dir * 80, 50, 80, self.x, self.y)

    def handle_events(self, event):
        global RIGHT, LEFT, UP, DOWN
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            RIGHT = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            LEFT = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            UP = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            DOWN = True
        if (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            RIGHT = False
        if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            LEFT = False
        if (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            UP = False
        if (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            DOWN = False
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            new_attack = Basic_attack()
            # dir 이 0이면 오른쪽 발사
            if self.dir == 0:
               new_attack.x, new_attack.y = self.x + 10, self. y
            # dir 이 1이면 왼쪽 발사
            elif self.dir == 1:
                new_attack.x, new_attack.y = self.x - 10, self.y
                new_attack.dir = 1
                new_attack.frame = 1
            basic_attacks.append(new_attack)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            new_attack = Missile_attack()
            if self.dir == 0:
                new_attack.x, new_attack.y = self.x + 10, self.y
            # dir 이 1이면 왼쪽 발사
            elif self.dir == 1:
                new_attack.x, new_attack.y = self.x - 10, self.y
                new_attack.dir = 1
                new_attack.frame = 1
            missile_attacks.append(new_attack)

    def get_bb(self):
        return self.x - 25, self.y - 45, self.x + 25, self.y + 45

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Basic_attack:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self):
        self.dir = 0
        self.frame = 0
        self.x, self.y = 0, 0
        if Basic_attack.image is None:
            Basic_attack.image = load_image("basic_attack.png")

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.move()

    def move(self):
        # dir 이 0 일때는 오른쪽으로 이동
        if self.dir == 0:
          self.x += self.runspeed
        # dir 이 1일 때는 왼쪽으로 이동
        elif self.dir == 1:
          self.x -= self.runspeed

    def draw(self):
        self.image.clip_draw(self.frame*40, 0, 40, 20, self.x, self.y)

    def get_bb(self):
        return self.x - 20, self.y - 10, self.x + 20, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Missile_attack:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 60.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self):
        self.dir = 0
        self.frame = 0
        if Missile_attack.image is None:
            Missile_attack.image = load_image("missile_attack.png")
        self.x, self.y = 0, 0

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.move()

    def move(self):
        # dir 이 0 일때는 오른쪽으로 이동
        if self.dir == 0:
          self.x += self.runspeed
        # dir 이 1일 때는 왼쪽으로 이동
        elif self.dir == 1:
          self.x -= self.runspeed

    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 20, self.x, self.y)

    def get_bb(self):
        return self.x - 25, self.y - 10, self.x + 25, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Attack_effect():
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x = 10
        self.y = 10
        self.frame = 0
        self.total_frames = 0
        if Attack_effect.image is None:
            self.image = load_image("attack_effect.png")

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 37, self.x, self.y)

class Attack_effect2():
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x = 10
        self.y = 10
        self.frame = 0
        self.total_frames = 0
        if Attack_effect.image is None:
            self.image = load_image("attack_effect2.png")

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y)