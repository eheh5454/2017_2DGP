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

soldier = None
ui = None
bullet_effects = None
missile_effects = None
special_attack_effects = None
eyemonsters = None
plantmonsters = None
powermonsters = None
swagemonsters = None
deleted_eyemonsters = None
deleted_powermonsters = None
deleted_plantmonsters = None
deleted_swagemonsters = None
background = None
stage1_BGM = None

# 시간에 따라 monster 를 만들어주는 함수
def make_all_monster(frame_time):
    global eyemonster_time, plantmonster_time, powermonster_time, swagemonster_time, eyemonsters, powermonsters, \
           plantmonsters, swagemonsters
    eyemonster_time += frame_time
    plantmonster_time += frame_time
    powermonster_time += frame_time
    swagemonster_time += frame_time
    if eyemonster_time > 5:
        if current_time > 30:
            new_eye_monster = Eyemonster()
            eyemonsters.append(new_eye_monster)
        new_eye_monster = Eyemonster()
        eyemonsters.append(new_eye_monster)
        eyemonster_time = 0
    if plantmonster_time > 10:
        if current_time > 60:
            new_plant_monster = Plantmonster()
            eyemonsters.append(new_plant_monster)
        new_plant_monster = Plantmonster()
        plantmonsters.append(new_plant_monster)
        plantmonster_time = 0
    if powermonster_time > 7:
        if current_time > 40:
            new_power_monster = Powermonster()
            powermonsters.append(new_power_monster)
        new_power_monster = Powermonster()
        powermonsters.append(new_power_monster)
        powermonster_time = 0
    if swagemonster_time > 7:
        if current_time > 50:
            new_swage_monster = Swagemonster()
            swagemonsters.append(new_swage_monster)
        new_swage_monster = Swagemonster()
        swagemonsters.append(new_swage_monster)
        swagemonster_time = 0


# 기본 충돌 체크 함수
def collision_check(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


# soldier 와 monster 의 충돌 처리
def collision_soldier_monster():
    global soldier, eyemonsters, plantmonsters, powermonsters, swagemonsters
    all_monsters = eyemonsters + plantmonsters + powermonsters + swagemonsters
    for monster in all_monsters:
        if collision_check(soldier, monster):
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
    global eyemonsters, plantmonsters, powermonsters, swagemonsters, missiles, bullets,\
           special_attack_effects, bomb_attacks
    all_monsters = eyemonsters + plantmonsters + powermonsters + swagemonsters
    # basic_attack 과 monster 의 충돌 처리
    for new_attack in bullets:
        for monster in all_monsters:
            if collision_check(new_attack, monster):
                new_attack_effect = Bullet_effect()
                new_attack_effect.x, new_attack_effect.y = new_attack.x, new_attack.y
                bullet_effects.append(new_attack_effect)
                if new_attack in bullets:
                   bullets.remove(new_attack)
                monster.hp -= 5
    # missile_attack 과 monster 의 충돌 처리
    for new_attack in missiles:
        for monster in all_monsters:
            if collision_check(new_attack, monster):
                new_attack_effect = Missile_effect()
                new_attack_effect.x, new_attack_effect.y = new_attack.x , new_attack.y
                missile_effects.append(new_attack_effect)
                if new_attack in missiles:
                   missiles.remove(new_attack)
                monster.hp -= 10
    # special_attack 과 monster 의 충돌 처리
    for new_attack in special_attack_effects:
        for monster in all_monsters:
            if collision_check(new_attack, monster):
                monster.hp -= 30
    for new_bomb_attack in bomb_attacks:
        for monster in all_monsters:
            if collision_check(new_bomb_attack, monster):
                new_special_attack_effect = Special_attack_effect()
                new_special_attack_effect.x, new_special_attack_effect.y = new_bomb_attack.x, new_bomb_attack.y
                bomb_attacks.remove(new_bomb_attack)
                special_attack_effects.append(new_special_attack_effect)


# 모든 몬스터 update, 몬스터가 죽으면 deleted 이펙트 그 좌표에 추가
def update_all_monster(frame_time):
    global Score, eyemonsters, plantmonsters, powermonsters, swagemonsters, \
           deleted_eyemonsters, deleted_powermonsters, deleted_plantmonsters, deleted_swagemonsters
    for new_eye_monster in eyemonsters:
        new_eye_monster.update(frame_time)
        if new_eye_monster.hp <= 0:
            new_deleted_em = Deleted_Eyemonster()
            new_deleted_em.x, new_deleted_em.y = new_eye_monster.x, new_eye_monster.y
            deleted_eyemonsters.append(new_deleted_em)
            eyemonsters.remove(new_eye_monster)
            Score += 5
    for new_plant_monster in plantmonsters:
        new_plant_monster.update(frame_time)
        if new_plant_monster.hp <= 0:
            new_deleted_plm = Deleted_Plantmonster()
            new_deleted_plm.x, new_deleted_plm.y = new_plant_monster.x, new_plant_monster.y
            deleted_plantmonsters.append(new_deleted_plm)
            plantmonsters.remove(new_plant_monster)
            Score += 10
    for new_power_monster in powermonsters:
        new_power_monster.update(frame_time)
        if new_power_monster.hp <= 0:
            new_deleted_pm = Deleted_Powermonster()
            new_deleted_pm.x, new_deleted_pm.y = new_power_monster.x, new_power_monster.y
            deleted_powermonsters.append(new_deleted_pm)
            powermonsters.remove(new_power_monster)
            Score += 7
    for new_swage_monster in swagemonsters:
        new_swage_monster.update(frame_time)
        if new_swage_monster.hp <= 0:
            new_deleted_sm = Deleted_Swagemonster()
            new_deleted_sm.x, new_deleted_sm.y = new_swage_monster.x, new_swage_monster.y
            deleted_swagemonsters.append(new_deleted_sm)
            swagemonsters.remove(new_swage_monster)
            Score += 6


# monster 들의 삭제 이펙트 업데이트
def deleted_effect_update(frame_time):
    global deleted_eyemonsters, deleted_powermonsters, deleted_plantmonsters, deleted_swagemonsters
    for deleted_em in deleted_eyemonsters:
        deleted_em.update(frame_time)
        if deleted_em.frame >= 3:
            deleted_eyemonsters.remove(deleted_em)
    for deleted_pm in deleted_powermonsters:
        deleted_pm.update(frame_time)
        if deleted_pm.frame >= 3:
            deleted_powermonsters.remove(deleted_pm)
    for deleted_plm in deleted_plantmonsters:
        deleted_plm.update(frame_time)
        if deleted_plm.frame >= 3:
            deleted_plantmonsters.remove(deleted_plm)
    for deleted_sm in deleted_swagemonsters:
        deleted_sm.update(frame_time)
        if deleted_sm.frame >= 2:
            deleted_swagemonsters.remove(deleted_sm)


# 모든 공격과 이펙트 update
def update_all_attack(frame_time):
    global bullets, missiles, bomb_attacks, bullet_effects, missile_effects, special_attacks, special_attack_effects
    for new_attack in bullets:
        new_attack.update(frame_time)
        if new_attack.x > 800 or new_attack.x < 0:
            del (new_attack)
    for new_attack in missiles:
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
    for attack_effect in bullet_effects:
        attack_effect.update(frame_time)
        if attack_effect.frame == 5:
            bullet_effects.remove(attack_effect)
    for attack_effect in missile_effects:
        attack_effect.update(frame_time)
        if attack_effect.frame == 5:
            missile_effects.remove(attack_effect)
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
    if bomb_item_time >= 10:
        new_item = Bomb_item()
        bomb_items.append(new_item)
        bomb_item_time = 0


# all item update
def update_all_items(frame_time):
    global soldier, special_attack_items, bomb_items
    for item in special_attack_items:
        item.update(frame_time)
        if collision_check(item, soldier):
            soldier.eat()
            soldier.special_attack_count += 1
            special_attack_items.remove(item)
    for item in bomb_items:
        item.update(frame_time)
        if collision_check(item, soldier):
            soldier.eat()
            soldier.bomb_count += 1
            bomb_items.remove(item)


# 모든 객체 draw
def draw_all():
    global space, soldier, eyemonsters, plantmonsters, powermonsters, bullet_effects, \
    deleted_eyemonsters, deleted_powermonsters, deleted_plantmonsters, swagemonsters, deleted_swagemonsters, missile_effects, special_attack_effects, ui
    all_attacks = bullets + missiles + bullet_effects + missile_effects + \
                  special_attacks + special_attack_effects + bomb_attacks
    all_deleted_effects = deleted_eyemonsters + deleted_powermonsters + deleted_plantmonsters + deleted_swagemonsters
    all_items = special_attack_items + bomb_items
    all_monsters = eyemonsters + plantmonsters + powermonsters + swagemonsters
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
        self.font = load_font('YGD360.TTF', 30)

    def draw(self):
        global special_attack_count, bomb_count
        self.font.draw(20, 550, 'Life:%d' % soldier.hp, (220, 220, 0))
        self.font.draw(20, 520, 'Score:%d' % Score, (220, 220, 0))
        self.font.draw(540, 550, "Special Attack:%d" % soldier.special_attack_count, (220, 220, 0))
        self.font.draw(670, 520, "Bomb:%d" % soldier.bomb_count, (220, 220, 0))


def enter():
    global space, soldier, eyemonsters, plantmonsters, powermonsters, bullet_effects,\
        deleted_eyemonsters, deleted_powermonsters, deleted_plantmonsters, swagemonsters, deleted_swagemonsters, \
        missile_effects, special_attack_effects, ui, background, stage1_BGM
    background = load_image("Space.jpg")
    soldier = Soldier()
    ui = UI()
    stage1_BGM = load_music("Stage1BGM.mp3")
    stage1_BGM.set_volume(64)
    stage1_BGM.repeat_play()
    bullet_effects = []
    missile_effects = []
    special_attack_effects = []
    eyemonsters = []
    plantmonsters = []
    powermonsters = []
    swagemonsters = []
    deleted_eyemonsters = []
    deleted_powermonsters = []
    deleted_plantmonsters = []
    deleted_swagemonsters = []


def exit():
    global soldier, eyemonsters, bullets, plantmonsters, powermonsters, bullet_effects, \
        deleted_eyemonsters, deleted_powermonsters, deleted_plantmonsters, swagemonsters, deleted_swagemonsters, missiles, missile_effects, \
        special_attacks, special_attack_effects, bomb_attacks, ui, special_attack_items, bomb_items, background, stage1_BGM
    del soldier
    del eyemonsters
    del bullets
    del plantmonsters
    del powermonsters
    del bullet_effects
    del missile_effects
    del missiles
    del swagemonsters
    del deleted_eyemonsters
    del deleted_powermonsters
    del deleted_plantmonsters
    del deleted_swagemonsters
    del special_attacks
    del special_attack_effects
    del bomb_attacks
    del ui
    del special_attack_items
    del bomb_items
    del background
    del stage1_BGM



def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            game_framework.change_state(Game_over)
        else:
            soldier.handle_events(event)


def update(frame_time):
    global current_time
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
    if soldier.hp <= 0:
        game_framework.change_state(Game_over)


def draw(frame_time):
    clear_canvas()
    background.draw(400, 300)
    draw_all()
    #soldier.draw_bb()
    update_canvas()

