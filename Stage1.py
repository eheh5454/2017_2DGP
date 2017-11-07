from pico2d import *

import game_framework
import random
from Resource import *

space = None
soldier = None

UP = False
DOWN = False
RIGHT = False
LEFT = False

monsters = []
counter = 0
eye_monster_count = 0

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

    def move(self):
        if UP:
          self.y += 10
        if DOWN:
          self.y -= 10
        if RIGHT:
          self.x += 10
        if LEFT:
          self.x -= 10

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.move()

    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 90, self.x, self.y)

    def handle_events(self,event):
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


class Eye_monster:
    def __init__(self):
        self.x, self.y = random.randint(50, 750), random.randint(50, 550)
        self.frame = 0
        self.image = load_image('Eye_monster.png')
        self.xmove = 10
        self.ymove = 10
        self.hp = 20

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
    global space, soldier, eye_monster, monsters
    del(space)
    del(soldier)
    del(eye_monster)
    del(monsters)


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
        else:
            soldier.handle_events(event)


def update():
    global counter,eye_monster_count
    soldier.update()
    eye_monster.update()
    for team in monsters:
        team.update()
    counter += 0.5
    if counter > 5 and eye_monster_count <= 10:
        new_eye_monster = Eye_monster()
        monsters.append(new_eye_monster)
        counter = 0
        eye_monster_count += 1



def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    eye_monster.draw()
    for new_eye_monster in monsters:
        new_eye_monster.draw()
    delay(0.05)
    update_canvas()
