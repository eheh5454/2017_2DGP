from pico2d import *
import game_framework
import random
import Game_over

from Resource import *
from Soldier import *
from Monsters import *
from Items import *

current_time = get_time()

Score = 0


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
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


# soldier 전용 추가 충돌체크 함수
def new_collison_check(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb2()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


# soldier 와 monster 의 충돌 처리
def collision_soldier_monster():
    all_monsters = eye_monsters + plant_monsters + power_monsters + swage_monsters
    for monster in all_monsters:
        if collision_check(soldier, monster) or new_collison_check(soldier, monster):
            # DAMAGED 상황일 때는 제외하고 충돌 처리, 충돌이 발생하면 state 를 DAMAGED 로 전환하고 frame 초기화
            if soldier.state in (soldier.RIGHT_RUN, soldier.RIGHT_ATTACK, soldier.RIGHT_THROW_BOMB):
                soldier.state = soldier.RIGHT_DAMAGED
                soldier.frame = 0
                monster.hp = 0
                soldier.hp -= monster.power
            elif soldier.state in (soldier.LEFT_RUN, soldier.LEFT_DAMAGED, soldier.LEFT_THROW_BOMB):
                soldier.state = soldier.LEFT_DAMAGED
                soldier.frame = 0
                monster.hp = 0
                soldier.hp -= monster.power


# attack 과 monster 의 충돌 처리
def collision_attack_monster():
    all_monsters = eye_monsters + plant_monsters + power_monsters + swage_monsters
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
    for new_bomb_attack in bomb_attacks:
        for monster in all_monsters:
            if collision_check(new_bomb_attack, monster):
                bomb_attacks.remove(new_bomb_attack)
                new_special_attack_effect = Special_attack_effect()
                new_special_attack_effect.x, new_special_attack_effect.y = new_bomb_attack.x, new_bomb_attack.y
                special_attack_effects.append(new_special_attack_effect)


# 모든 몬스터 update, 몬스터가 죽으면 deleted 이펙트 그 좌표에 추가
def update_all_monster(frame_time):
    global Score
    for new_eye_monster in eye_monsters:
        new_eye_monster.update(frame_time)
        if new_eye_monster.hp <= 0:
            new_deleted_em = Deleted_em()
            new_deleted_em.x, new_deleted_em.y = new_eye_monster.x, new_eye_monster.y
            deleted_ems.append(new_deleted_em)
            eye_monsters.remove(new_eye_monster)
            Score += 5
    for new_plant_monster in plant_monsters:
        new_plant_monster.update(frame_time)
        if new_plant_monster.hp <= 0:
            new_deleted_plm = Deleted_plm()
            new_deleted_plm.x, new_deleted_plm.y = new_plant_monster.x, new_plant_monster.y
            deleted_plms.append(new_deleted_plm)
            plant_monsters.remove(new_plant_monster)
            Score += 10
    for new_power_monster in power_monsters:
        new_power_monster.update(frame_time)
        if new_power_monster.hp <= 0:
            new_deleted_pm = Deleted_pm()
            new_deleted_pm.x, new_deleted_pm.y = new_power_monster.x, new_power_monster.y
            deleted_pms.append(new_deleted_pm)
            power_monsters.remove(new_power_monster)
            Score += 7
    for new_swage_monster in swage_monsters:
        new_swage_monster.update(frame_time)
        if new_swage_monster.hp <= 0:
            new_deleted_sm = Deleted_sm()
            new_deleted_sm.x, new_deleted_sm.y = new_swage_monster.x, new_swage_monster.y
            deleted_sms.append(new_deleted_sm)
            swage_monsters.remove(new_swage_monster)
            Score += 6


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


def make_items(frame_time):
    global special_attack_items_time, bomb_item_time
    special_attack_items_time += frame_time
    bomb_item_time += frame_time
    if special_attack_items_time >= 10:
        new_item = Special_attack_item()
        special_attack_items.append(new_item)
        special_attack_items_time = 0
    if bomb_item_time >= 5:
        new_item = Bomb_item()
        bomb_items.append(new_item)
        bomb_item_time = 0


def update_all_items(frame_time):
    for item in special_attack_items:
        item.update(frame_time)
        if collision_check(item, soldier):
            soldier.special_attack_count += 1
            special_attack_items.remove(item)
    for item in bomb_items:
        item.update(frame_time)
        if collision_check(item, soldier):
            soldier.bomb_count += 1
            bomb_items.remove(item)


# 모든 객체 draw
def draw_all():
    all_attacks = basic_attacks + missile_attacks + attack_effects + attack_effects2 + \
                  special_attacks + special_attack_effects + bomb_attacks
    all_deleted_effects = deleted_ems + deleted_pms + deleted_plms + deleted_sms
    all_items = special_attack_items + bomb_items
    all_monsters = eye_monsters + plant_monsters + power_monsters + swage_monsters
    space.draw()
    soldier.draw()
    for attack in all_attacks:
        attack.draw()
    for item in all_items:
        item.draw()
    for deleted_effect in all_deleted_effects:
        deleted_effect.draw()
    for monster in all_monsters:
        monster.draw()
    ui.draw()


class UI():
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 30)

    def draw(self):
        global special_attack_count, bomb_count
        self.font.draw(20, 550, 'Life:%d' % soldier.hp, (220, 220, 0))
        self.font.draw(20, 520, 'Score:%d' % Score, (220, 220, 0))
        self.font.draw(500, 550, "Special Attack:%d" % soldier.special_attack_count, (220, 220, 0))
        self.font.draw(680, 520, "Bomb:%d" % soldier.bomb_count, (220, 220, 0))


def enter():
    global space, soldier, eye_monsters, plant_monsters, power_monsters, attack_effects,\
        deleted_ems, deleted_pms, deleted_plms, swage_monsters, deleted_sms, attack_effects2, special_attack_effects, ui
    space = Space()
    soldier = Soldier()
    ui = UI()
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
        special_attacks, special_attack_effects, bomb_attacks, ui, special_attack_items
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
    del ui
    del special_attack_items


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            game_framework.change_state(Game_over)
        else:
            soldier.handle_events(event)


def update():
    global current_time
    frame_time = get_time() - current_time
    if soldier.hp <= 0:
        game_framework.change_state(Game_over)
    collision_attack_monster()
    collision_soldier_monster()
    soldier.update(frame_time)
    make_all_monster(frame_time)
    update_all_monster(frame_time)
    deleted_effect_update(frame_time)
    update_all_attack(frame_time)
    make_items(frame_time)
    update_all_items(frame_time)
    current_time += frame_time


def draw():
    clear_canvas()
    draw_all()
    #soldier.draw_bb()
    update_canvas()

