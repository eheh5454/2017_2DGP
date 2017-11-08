from pico2d import *
import game_framework
import random

from Resource import *
from Soldier import *
from Monsters import *


timecounter = 0
eye_monster_count = 0

class Space:
    def __init__(self):
        self.image = load_image('Space.jpg')

    def draw(self):
        self.image.draw(400, 300)

def enter():
    global space, soldier, eye_monster, eye_monsters
    space = Space()
    soldier = Soldier()
    eye_monster = Eye_monster()
    eye_monsters = []


def exit():
    global space, soldier, eye_monster, monsters, eye_monsters, basic_attacks
    del(space)
    del(soldier)
    del(eye_monster)
    del(eye_monsters)
    del(basic_attacks)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            soldier.handle_events(event)


def update():
    global timecounter, eye_monster_count
    soldier.update()
    eye_monster.update()
    for team in eye_monsters:
        team.update()
    timecounter += 0.5
    if timecounter > 10 and eye_monster_count <= 10:
        new_eye_monster = Eye_monster()
        eye_monsters.append(new_eye_monster)
        timecounter = 0
        eye_monster_count += 1
    for new_attack in basic_attacks:
        new_attack.update()
        if new_attack.x > 800:
            del(new_attack)


def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    eye_monster.draw()
    for new_attack in basic_attacks:
        new_attack.draw()
    for new_eye_monster in eye_monsters:
        new_eye_monster.draw()
    delay(0.05)
    update_canvas()
