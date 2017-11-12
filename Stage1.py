from pico2d import *
import game_framework
import random

from Resource import *
from Soldier import *
from Monsters import *

current_time = get_time()
eye_monster_count = 0
eye_monstertime = 0
plant_monster_count = 0
plant_monstertime = 0
power_monster_count = 0
power_monstertime = 0

#맵크기 = 800X600픽셀 즉 1600cm x 1200cm 16m x 12m
class Space:
    def __init__(self):
        self.image = load_image('Space.jpg')

    def draw(self):
        self.image.draw(400, 300)


def enter():
    global space, soldier, eye_monsters, plant_monsters, power_monsters
    space = Space()
    soldier = Soldier()
    eye_monsters = []
    plant_monsters = []
    power_monsters = []


def exit():
    global space, soldier, eye_monsters, basic_attacks, plant_monsters, power_monsters
    del(space)
    del(soldier)
    del(eye_monsters)
    del(basic_attacks)
    del(plant_monsters)
    del(power_monsters)


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


def make_eye_monster(frame_time):
    global eye_monstertime, eye_monster_count
    eye_monstertime += frame_time
    if eye_monstertime > 5 and eye_monster_count <= 10:
            new_eye_monster = Eye_monster()
            eye_monsters.append(new_eye_monster)
            eye_monstertime = 0
            eye_monster_count += 1

def make_plant_monster(frame_time):
    global plant_monstertime, plant_monster_count
    plant_monstertime += frame_time
    if plant_monstertime > 7 and plant_monster_count <= 5:
        new_plant_monster = Plant_monster()
        plant_monsters.append(new_plant_monster)
        plant_monstertime = 0
        plant_monster_count += 1

def make_power_monster(frame_time):
    global power_monstertime, power_monster_count
    power_monstertime += frame_time
    if power_monstertime > 5 and power_monster_count <= 7:
        new_power_monster = Power_monster()
        power_monsters.append(new_power_monster)
        power_monstertime = 0
        power_monster_count += 1

def update():
    global current_time
    frame_time = get_time() - current_time
    soldier.update(frame_time)
    make_eye_monster(frame_time)
    make_plant_monster(frame_time)
    make_power_monster(frame_time)
    for new_eye_monster in eye_monsters:
        new_eye_monster.update(frame_time)
    for new_plant_monster in plant_monsters:
        new_plant_monster.update(frame_time)
    for new_power_monster in power_monsters:
        new_power_monster.update(frame_time)
    for new_attack in basic_attacks:
        new_attack.update(frame_time)
        if new_attack.x > 800:
            del(new_attack)

    current_time += frame_time


def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    for new_attack in basic_attacks:
        new_attack.draw()
    for new_eye_monster in eye_monsters:
        new_eye_monster.draw()
    for new_plant_monster in plant_monsters:
        new_plant_monster.draw()
    for new_power_monster in power_monsters:
        new_power_monster.draw()

    update_canvas()
