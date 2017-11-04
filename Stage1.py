from pico2d import *

import game_framework
from Resource import *

space = None
soldier = None

UP = False
DOWN = False
RIGHT = False
LEFT = False


class Space:
    def __init__(self):
        self.image = load_image('Space.jpg')

    def draw(self):
        self.image.draw(400, 300)


class Soldier:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.image = load_image('soldier.png')
        self.hp = 50

    def UP_MOVE(self):
        if UP:
          self.y += 10

    def DOWN_MOVE(self):
        if DOWN:
          self.y -= 10

    def RIGHT_MOVE(self):
        if RIGHT:
          self.x += 10

    def LEFT_MOVE(self):
        if LEFT:
          self.x -= 10

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.DOWN_MOVE()
        self.UP_MOVE()
        self.RIGHT_MOVE()
        self.LEFT_MOVE()

    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 90, self.x, self.y)


class Eye_monster:
    def __init__(self):
        self.x, self.y = 50, 50
        self.frame = 0
        self.image = load_image('Eye_monster.png')
        self.xmove = 10
        self.ymove = 10

    def update(self):
        self.frame = (self.frame + 1) % 7
        self.move()



    def draw(self):
        self.image.clip_draw(self.frame*70, 0, 70, 70, self.x, self.y)

    def move(self):
        self.x += self.xmove
        self.y += self.ymove
        if self.x > 800:
            self.xmove = -self.xmove
        if self.x < 0:
            self.xmove = -self.xmove
        if self.y > 600:
            self.ymove = -self.ymove
        if self.y < 0:
            self.ymove = -self.ymove


def enter():
    global space, soldier, eye_monster
    space = Space()
    soldier = Soldier()
    eye_monster = Eye_monster()


def exit():
    global space, soldier, eye_monster
    del(space)
    del(soldier)
    del(eye_monster)


def pause():
    pass


def resume():
    pass


def handle_events():
    global UP, DOWN, RIGHT, LEFT, soldier
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            UP = True
        elif event.type == SDL_KEYUP and event.key == SDLK_UP:
            UP = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            DOWN = True
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            DOWN = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            RIGHT = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            RIGHT = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            LEFT = True
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            LEFT = False


def update():
    soldier.update()
    eye_monster.update()


def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    eye_monster.draw()
    delay(0.05)
    update_canvas()
