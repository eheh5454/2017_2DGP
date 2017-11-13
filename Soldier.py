from pico2d import *
import random

space = None
soldier = None

UP = False
DOWN = False
RIGHT = False
LEFT = False

basic_attacks = []


# soldier의 크기 = 50 x 90픽셀, 키 180cm
class Soldier:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x, self.y = 400, 300
        if self.image == None:
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
        if LEFT:
          self.x -= self.runspeed

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME *frame_time
        self.frame = int(self.total_frames) % 8
        self.move()

    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 90, self.x, self.y)

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
            new_attack.x = self.x +10
            new_attack.y = self.y
            basic_attacks.append(new_attack)
            pass

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
        if self.image == None:
           self.image = load_image("Basic_attack.png")
        self.x, self.y = 0, 0

    def update(self,frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.right_move()

    def right_move(self):
        self.x += self.runspeed

    def left_move(self):
        self.x -= self.runspeed

    def up_move(self):
        self.y += self.runspeed

    def down_move(self):
        self.y -= self.runspeed

    def draw(self):
        self.image.draw(self.x,self.y)

    def get_bb(self):
        return self.x - 20, self.y - 10, self.x + 20, self.y + 10

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
        if self.image == None:
            self.image = load_image("attack_effect.png")

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 37, self.x, self.y)