from pico2d import *
import random

space = None
soldier = None

UP = False
DOWN = False
RIGHT = False
LEFT = False

basic_attacks = []

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

class Basic_attack:
    def __init__(self):
        self.image = load_image("Basic_attack.png")
        self.x, self.y = 0, 0

    def update(self):
        self.right_move()

    def right_move(self):
        self.x += 15

    def left_move(self):
        self.x -= 15

    def up_move(self):
        self.y += 15

    def down_move(self):
        self.y -= 15

    def draw(self):
        self.image.draw(self.x,self.y)