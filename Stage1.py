from pico2d import *
import game_framework
import random

from Resource import *
from Soldier import *
from Monsters import *
import json

current_time = get_time()
eye_monstertime = 0
plant_monstertime = 0
power_monstertime = 0
swage_monstertime = 0

# 맵크기 = 800X600픽셀, 1600cm x 1200cm, 16m x 12m
class Space:
    def __init__(self):
        self.image = load_image('Space.jpg')

    def draw(self):
        self.image.draw(400, 300)


# 시간에 따라 monster 를 만들어주는 함수
def make_all_monster(frame_time):
    global eye_monstertime, plant_monstertime, power_monstertime, swage_monstertime
    eye_monstertime += frame_time
    plant_monstertime += frame_time
    power_monstertime += frame_time
    swage_monstertime += frame_time
    if eye_monstertime > 5:
        new_eye_monster = Eye_monster()
        eye_monsters.append(new_eye_monster)
        eye_monstertime = 0
    if plant_monstertime > 10:
        new_plant_monster = Plant_monster()
        plant_monsters.append(new_plant_monster)
        plant_monstertime = 0
    if power_monstertime > 7:
        new_power_monster = Power_monster()
        power_monsters.append(new_power_monster)
        power_monstertime = 0
    if swage_monstertime > 7:
        new_swage_monster = Swage_monster()
        swage_monsters.append(new_swage_monster)
        swage_monstertime = 0


# 기본 충돌 체크 함수
def collision_check(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b : return False
    if bottom_a > top_b: return False

    return True


# soldier 와 monster 의 충돌 처리
def collision_soldier_monster():
    all_monster = eye_monsters + power_monsters + plant_monsters + swage_monsters
    for monster in all_monster:
        if collision_check(monster, soldier):
            # DAMAGED 상황일 때는 제외하고 충돌 처리, 충돌이 발생하면 state 를 DAMAGED 로 전환하고 frame 초기화
            if soldier.state == (soldier.RIGHT_RUN or soldier.RIGHT_ATTACK or soldier.RIGHT_THROW_BOMB):
                soldier.state = soldier.RIGHT_DAMAGED
                soldier.frame = 0
                soldier.hp -= 5
            if soldier.state == (soldier.LEFT_RUN or soldier.LEFT_DAMAGED or soldier.LEFT_THROW_BOMB):
                soldier.state = soldier.LEFT_DAMAGED
                soldier.frame = 0
                soldier.hp -= 5


# attack 과 monster 의 충돌 처리
def collision_attack_monster():
    all_monsters = power_monsters + eye_monsters + swage_monsters + plant_monsters
    # basic_attack 과 monster 의 충돌 처리
    for new_attack in basic_attacks:
        for monster in all_monsters:
            if collision_check(new_attack, monster):
                new_attack_effect = Attack_effect()
                new_attack_effect.x, new_attack_effect.y = new_attack.x, new_attack.y
                attack_effects.append(new_attack_effect)
                if new_attack in basic_attacks:
                   basic_attacks.remove(new_attack)
                monster.hp -= 5
    # missile_attack 과 monster 의 충돌 처리
    for new_attack in missile_attacks:
        for monster in all_monsters:
            if collision_check(new_attack, monster):
                new_attack_effect = Attack_effect2()
                new_attack_effect.x, new_attack_effect.y = new_attack.x , new_attack.y
                attack_effects2.append(new_attack_effect)
                if new_attack in missile_attacks:
                   missile_attacks.remove(new_attack)
                monster.hp -= 10
    # special_attack 과 monster 의 충돌 처리
    for new_attack in special_attack_effects:
        for monster in all_monsters:
            if collision_check(new_attack, monster):
                monster.hp -= 30


# 모든 몬스터 update, 몬스터가 죽으면 deleted 이펙트 그 좌표에 추가
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
            new_deleted_plm = Deleted_plm()
            new_deleted_plm.x, new_deleted_plm.y = new_plant_monster.x, new_plant_monster.y
            deleted_plms.append(new_deleted_plm)
            plant_monsters.remove(new_plant_monster)
    for new_power_monster in power_monsters:
        new_power_monster.update(frame_time)
        if new_power_monster.hp <= 0:
            new_deleted_pm = Deleted_pm()
            new_deleted_pm.x, new_deleted_pm.y = new_power_monster.x, new_power_monster.y
            deleted_pms.append(new_deleted_pm)
            power_monsters.remove(new_power_monster)
    for new_swage_monster in swage_monsters:
        new_swage_monster.update(frame_time)
        if new_swage_monster.hp <= 0:
            new_deleted_sm = Deleted_sm()
            new_deleted_sm.x, new_deleted_sm.y = new_swage_monster.x, new_swage_monster.y
            deleted_sms.append(new_deleted_sm)
            swage_monsters.remove(new_swage_monster)


# 모든 몬스터 draw
def draw_all_monster():
    all_monsters = eye_monsters + power_monsters + plant_monsters + swage_monsters
    for monster in all_monsters:
        monster.draw()


# monster 들의 삭제 이펙트 업데이트
def deleted_effect_update(frame_time):
    for deleted_em in deleted_ems:
        deleted_em.update(frame_time)
        if deleted_em.frame >= 3:
            deleted_ems.remove(deleted_em)
    for deleted_pm in deleted_pms:
        deleted_pm.update(frame_time)
        if deleted_pm.frame >= 3:
            deleted_pms.remove(deleted_pm)
    for deleted_plm in deleted_plms:
        deleted_plm.update(frame_time)
        if deleted_plm.frame >= 3:
            deleted_plms.remove(deleted_plm)
    for deleted_sm in deleted_sms:
        deleted_sm.update(frame_time)
        if deleted_sm.frame >= 2:
            deleted_sms.remove(deleted_sm)


# monster 들의 삭제 이펙트 그리기
def deleted_effect_draw():
    all_deleted_effects = deleted_ems + deleted_pms + deleted_plms + deleted_sms
    for deleted_effect in all_deleted_effects:
        deleted_effect.draw()


# 모든 공격과 이펙트 update
def update_all_attack(frame_time):
    for new_attack in basic_attacks:
        new_attack.update(frame_time)
        if new_attack.x > 800 or new_attack.x < 0:
            del (new_attack)
    for new_attack in missile_attacks:
        new_attack.update(frame_time)
        if new_attack.x > 800 or new_attack.x < 0:
            del (new_attack)
    for new_bomb_attack in bomb_attacks:
        new_bomb_attack.update(frame_time)
        if new_bomb_attack.frame == 4:
            bomb_attacks.remove(new_bomb_attack)
            new_special_attack_effect = Special_attack_effect()
            new_special_attack_effect.x, new_special_attack_effect.y = new_bomb_attack.x, new_bomb_attack.y
            special_attack_effects.append(new_special_attack_effect)
    for attack_effect in attack_effects:
        attack_effect.update(frame_time)
        if attack_effect.frame == 5:
            attack_effects.remove(attack_effect)
    for attack_effect in attack_effects2:
        attack_effect.update(frame_time)
        if attack_effect.frame == 5:
            attack_effects2.remove(attack_effect)
    for new_attack in special_attacks:
        new_attack.update(frame_time)
        if new_attack.frame == 6:
            special_attacks.remove(new_attack)
            new_special_attack_effect = Special_attack_effect()
            new_special_attack_effect.x, new_special_attack_effect.y = new_attack.x, new_attack.y
            special_attack_effects.append(new_special_attack_effect)
    for new_special_attack_effect in special_attack_effects:
        new_special_attack_effect.update(frame_time)
        if new_special_attack_effect.frame == 6:
            special_attack_effects.remove(new_special_attack_effect)



# 모든 공격과 이펙트 draw
def draw_all_attack():
    all_attacks = basic_attacks + missile_attacks + attack_effects + attack_effects2 + \
                  special_attacks + special_attack_effects + bomb_attacks
    for attack in all_attacks:
        attack.draw()


def enter():
    global space, soldier, eye_monsters, plant_monsters, power_monsters, attack_effects, \
        deleted_ems, deleted_pms, deleted_plms, swage_monsters, deleted_sms, attack_effects2, special_attack_effects
    space = Space()
    soldier = Soldier()
    attack_effects = []
    attack_effects2 = []
    special_attack_effects = []
    eye_monsters = []
    plant_monsters = []
    power_monsters = []
    swage_monsters = []
    deleted_ems = []
    deleted_pms = []
    deleted_plms = []
    deleted_sms = []



def exit():
    global space, soldier, eye_monsters, basic_attacks, plant_monsters, power_monsters, attack_effects, \
        deleted_ems, deleted_pms, deleted_plms, swage_monsters, deleted_sms, missile_attacks, attack_effects2, \
        special_attacks, special_attack_effects, bomb_attacks
    del space
    del soldier
    del eye_monsters
    del basic_attacks
    del plant_monsters
    del power_monsters
    del attack_effects
    del attack_effects2
    del missile_attacks
    del swage_monsters
    del deleted_ems
    del deleted_pms
    del deleted_plms
    del deleted_sms
    del special_attacks
    del special_attack_effects
    del bomb_attacks


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
    update_all_attack(frame_time)
    collision_soldier_monster()
    current_time += frame_time


def draw():
    clear_canvas()
    space.draw()
    soldier.draw()
    draw_all_monster()
    draw_all_attack()
    deleted_effect_draw()
    update_canvas()
