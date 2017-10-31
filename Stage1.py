from pico2d import *

import game_framework
from Resource import *

space = None
soldier = None


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

    def update(self):
        self.frame = (self.frame + 1) % 8
        delay(0.05)

    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 90, self.x, self.y)



def enter():
    global space, soldier
    space = Space()
    soldier = Soldier()


def exit():
    global space, soldier
    del(space)
    del(soldier)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            soldier.y += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            soldier.y -= 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            soldier.x += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            soldier.x -= 10


def update():
    soldier.update()


def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    update_canvas()
