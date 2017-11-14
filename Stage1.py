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


# 맵크기 = 800X600픽셀, 1600cm x 1200cm, 16m x 12m
class Space:
    def __init__(self):
        self.image = load_image('Space.jpg')

    def draw(self):
        self.image.draw(400, 300)


# 시간에 따라 monster 를 만들어주는 함수
def make_all_monster(frame_time):
    global eye_monstertime, eye_monster_count, plant_monstertime, plant_monster_count, power_monstertime, power_monster_count
    eye_monstertime += frame_time
    plant_monstertime += frame_time
    power_monstertime += frame_time
    if eye_monstertime > 5 and eye_monster_count <= 10:
        new_eye_monster = Eye_monster()
        eye_monsters.append(new_eye_monster)
        eye_monstertime = 0
        eye_monster_count += 1
    if plant_monstertime > 7 and plant_monster_count <= 5:
        new_plant_monster = Plant_monster()
        plant_monsters.append(new_plant_monster)
        plant_monstertime = 0
        plant_monster_count += 1
    if power_monstertime > 5 and power_monster_count <= 7:
        new_power_monster = Power_monster()
        power_monsters.append(new_power_monster)
        power_monstertime = 0
        power_monster_count += 1

# 기본 충돌 체크 함수
def collision_check(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b : return False
    if bottom_a > top_b: return False

    return True

# 공격 이펙트를 추가하는 함수
def append_attack_effect(new_attack):
    global attack_effects, basic_attacks
    new_attack_effect = Attack_effect()
    new_attack_effect.x, new_attack_effect.y = new_attack.x + 20, new_attack.y
    attack_effects.append(new_attack_effect)
    basic_attacks.remove(new_attack)


def collision_soldier_monster():
    pass


# attack 과 monster 의 충돌 처리
def collision_attack_monster():
    global basic_attacks, eye_monsters, plant_monsters, power_monsters, attack_effects
    # basic_attack 과 eye_monster 의 충돌 체크
    for new_attack in basic_attacks:
        for eye_monster in eye_monsters:
            if collision_check(new_attack, eye_monster):
                new_attack_effect = Attack_effect()
                new_attack_effect.x, new_attack_effect.y = new_attack.x + 20, new_attack.y
                attack_effects.append(new_attack_effect)
                if new_attack in basic_attacks:
                   basic_attacks.remove(new_attack)
                eye_monster.hp -= 5
    # basic_attack 과 plant_monster 의 충돌 체크
    for new_attack in basic_attacks:
        for plant_monster in plant_monsters:
            if collision_check(new_attack, plant_monster):
                new_attack_effect = Attack_effect()
                new_attack_effect.x, new_attack_effect.y = new_attack.x + 20, new_attack.y
                attack_effects.append(new_attack_effect)
                if new_attack in basic_attacks:
                   basic_attacks.remove(new_attack)
                plant_monster.hp -= 5
    # basic_attack 과 power_monster 의 충돌 체크
    for new_attack in basic_attacks:
        for power_monster in power_monsters:
            if collision_check(new_attack, power_monster):
                new_attack_effect = Attack_effect()
                new_attack_effect.x, new_attack_effect.y = new_attack.x + 20, new_attack.y
                attack_effects.append(new_attack_effect)
                if new_attack in basic_attacks:
                   basic_attacks.remove(new_attack)
                power_monster.hp -= 5


def update_all_monster(frame_time):
    collision_attack_monster()
    for new_eye_monster in eye_monsters:
        new_eye_monster.update(frame_time)
        if new_eye_monster.hp <= 0:
            new_deleted_em = Deleted_em()
            new_deleted_em.x, new_deleted_em.y = new_eye_monster.x, new_eye_monster.y
            deleted_ems.append(new_deleted_em)
            eye_monsters.remove(new_eye_monster)
    for new_plant_monster in plant_monsters:
        new_plant_monster.update(frame_time)
        if new_plant_monster.hp <= 0:
            plant_monsters.remove(new_plant_monster)
    for new_power_monster in power_monsters:
        new_power_monster.update(frame_time)
        if new_power_monster.hp <= 0:
            new_deleted_pm = Deleted_pm()
            new_deleted_pm.x, new_deleted_pm.y = new_power_monster.x, new_power_monster.y
            deleted_pms.append(new_deleted_pm)
            power_monsters.remove(new_power_monster)


def draw_all_monster():
    for new_eye_monster in eye_monsters:
        new_eye_monster.draw()
        #new_eye_monster.draw_bb()
    for new_plant_monster in plant_monsters:
        new_plant_monster.draw()
        #new_plant_monster.draw_bb()
    for new_power_monster in power_monsters:
        new_power_monster.draw()
        #new_power_monster.draw_bb()

# monster 들의 삭제 이펙트 업데이트
def deleted_effect_update(frame_time):
    for deleted_em in deleted_ems:
        deleted_em.update(frame_time)
        if deleted_em.time >= 1.0:
            deleted_ems.remove(deleted_em)
    for deleted_pm in deleted_pms:
        deleted_pm.update(frame_time)
        if deleted_pm.time >= 1.0:
            deleted_pms.remove(deleted_pm)

# monster 들의 삭제 이펙트 그리기 ㅁ
def deleted_effect_draw():
    for deleted_em in deleted_ems:
        deleted_em.draw()
    for deleted_pm in deleted_pms:
        deleted_pm.draw()

def enter():
    global space, soldier, eye_monsters, plant_monsters, power_monsters, attack_effects, deleted_ems, deleted_pms
    space = Space()
    soldier = Soldier()
    attack_effects = []
    eye_monsters = []
    plant_monsters = []
    power_monsters = []
    deleted_ems = []
    deleted_pms = []


def exit():
    global space, soldier, eye_monsters, basic_attacks, plant_monsters, power_monsters, attack_effects, deleted_ems, deleted_pms
    del(space)
    del(soldier)
    del(eye_monsters)
    del(basic_attacks)
    del(plant_monsters)
    del(power_monsters)
    del(attack_effects)
    del(deleted_ems)
    del(deleted_pms)



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
    global current_time
    frame_time = get_time() - current_time
    soldier.update(frame_time)
    make_all_monster(frame_time)
    update_all_monster(frame_time)
    deleted_effect_update(frame_time)
    for new_attack in basic_attacks:
        new_attack.update(frame_time)
        if new_attack.x > 800:
            del(new_attack)
    for attack_effect in attack_effects:
        attack_effect.update(frame_time)
        if attack_effect.frame == 5:
            attack_effects.remove(attack_effect)
    current_time += frame_time


def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    #soldier.draw_bb()
    draw_all_monster()
    deleted_effect_draw()
    for new_attack in basic_attacks:
        new_attack.draw()
        #new_attack.draw_bb()
    for attack_effect in attack_effects:
        attack_effect.draw()
    update_canvas()
