from pico2d import *
import json

basic_attacks = []
missile_attacks = []
special_attacks = []

special_attack_text = '{ \
    "attack1" : {"x":50, "y":550},"attack2" : {"x":150, "y":550},"attack3" : {"x":250, "y":550},"attack4" : {"x":350, "y":550},\
    "attack5" : {"x":450, "y":550},"attack6" : {"x":550, "y":550},"attack7" : {"x":650, "y":550},"attack8" : {"x":750, "y":550},\
    "attack9" : {"x":50, "y":400},"attack10" : {"x":150, "y":400},"attack11" : {"x":250, "y":400},"attack12" : {"x":350, "y":400},\
    "attack13" : {"x":450, "y":400},"attack14" : {"x":550, "y":400},"attack15" : {"x":650, "y":400},"attack16" : {"x":750, "y":400},\
    "attack17" : {"x":50, "y":250},"attack18" : {"x":150, "y":250},"attack19" : {"x":250, "y":250},"attack20" : {"x":350, "y":250},\
    "attack21" : {"x":450, "y":250},"attack22" : {"x":550, "y":250},"attack23" : {"x":650, "y":250},"attack24" : {"x":750, "y":250},\
    "attack25" : {"x":50, "y":100},"attack26" : {"x":150, "y":100},"attack27" : {"x":250, "y":100},"attack28" : {"x":350, "y":100},\
    "attack29" : {"x":450, "y":100},"attack30" : {"x":550, "y":100},"attack31" : {"x":650, "y":100},"attack32" : {"x":750, "y":100}\
}'


# soldier 의 크기 = 50 x 80픽셀, 키 160cm
class Soldier:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    RIGHT_RUN, LEFT_RUN, RIGHT_DAMAGED, LEFT_DAMAGED = 0, 1, 2, 3
    RIGHT_ATTACK, LEFT_ATTACK, RIGHT_THROW_BOMB, LEFT_THROW_BOMB = 4, 5, 6, 7

    UP, DOWN, RIGHT, LEFT = False, False, False, False

    def __init__(self):
        self.x, self.y = 400, 300
        self.state = self.RIGHT_RUN
        self.image = load_image('soldier2.png')
        self.frame = 0
        self.total_frames = 0
        self.hp = 50

    def move(self):
        if self.UP:
            self.y += self.runspeed
        if self.DOWN:
            self.y -= self.runspeed
        if self.RIGHT:
            self.x += self.runspeed
            self.state = self.RIGHT_RUN
        if self.LEFT:
            self.x -= self.runspeed
            self.state = self.LEFT_RUN

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME *frame_time
        self.frame = int(self.total_frames) % 6
        self.move()
        # 오른쪽 데미지를 입었을때 프레임이 5가 되면 오른쪽 달리기 상태로 전환
        if self.state == self.RIGHT_DAMAGED and self.frame == 5:
            self.state = self.RIGHT_RUN
        # 왼쪽 데미지를 입었을떄 프레임이 5가 되면 왼쪽 달리기 상태로 전환
        if self.state == self.LEFT_DAMAGED and self.frame == 5:
            self.state = self.LEFT_RUN

    def draw(self):
        self.image.clip_draw(self.frame*50, self.state * 80, 50, 80, self.x, self.y)

    def handle_events(self, event):
        global RIGHT, LEFT, UP, DOWN
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.RIGHT = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.LEFT = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.UP = True
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.DOWN = True
        if (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.RIGHT = False
        if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            self.LEFT = False
        if (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            self.UP = False
        if (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            self.DOWN = False
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            new_attack = Basic_attack()
            # RIGHT_RUN state 이면 오른쪽 발사
            if self.state == self.RIGHT_RUN:
               new_attack.x, new_attack.y = self.x + 10, self. y
               self.state = self.RIGHT_ATTACK
            # LEFT_RUN state 이면 왼쪽 발사
            elif self.state == self.LEFT_RUN:
                new_attack.x, new_attack.y = self.x - 10, self.y
                new_attack.dir = 1
                new_attack.frame = 1
                self.state = self.LEFT_ATTACK
            basic_attacks.append(new_attack)
        # a키를 놓을 때는 공격상태에서 원래 상태로 전환
        if (event.type, event.key) == (SDL_KEYUP, SDLK_a):
            if self.state == self.RIGHT_ATTACK:
                self.state = self.RIGHT_RUN
            elif self.state == self.LEFT_ATTACK:
                self.state = self.LEFT_RUN
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            new_attack = Missile_attack()
            # RIGHT_RUN state 이면 오른쪽 발사
            if self.state == self.RIGHT_RUN:
                new_attack.x, new_attack.y = self.x + 10, self.y
            # LEFT_RUN state 이면 왼쪽 발사
            elif self.state == self.LEFT_RUN:
                new_attack.x, new_attack.y = self.x - 10, self.y
                new_attack.dir = 1
                new_attack.frame = 1
            missile_attacks.append(new_attack)
        # 필살기 사용
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            #special_attack_file = open('special_attack_data.txt', 'r')
            #special_attack_data = json.load(special_attack_file)
            #special_attack_file.close()
            special_attack_data = json.loads(special_attack_text)
            for data in special_attack_data:
                special_attack = Special_attack()
                special_attack.x = special_attack_data[data]['x']
                special_attack.y = special_attack_data[data]['y']
                special_attacks.append(special_attack)

    def get_bb(self):
        return self.x - 25, self.y - 45, self.x + 25, self.y + 45

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Basic_attack:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self):
        self.dir = 0
        self.frame = 0
        self.x, self.y = 0, 0
        if Basic_attack.image is None:
            Basic_attack.image = load_image("basic_attack.png")

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.move()

    def move(self):
        # dir 이 0 일때는 오른쪽으로 이동
        if self.dir == 0:
          self.x += self.runspeed
        # dir 이 1일 때는 왼쪽으로 이동
        elif self.dir == 1:
          self.x -= self.runspeed

    def draw(self):
        self.image.clip_draw(self.frame*40, 0, 40, 20, self.x, self.y)

    def get_bb(self):
        return self.x - 20, self.y - 10, self.x + 20, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Missile_attack:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 60.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self):
        self.dir = 0
        self.frame = 0
        if Missile_attack.image is None:
            Missile_attack.image = load_image("missile_attack.png")
        self.x, self.y = 0, 0

    def update(self, frame_time):
        self.runspeed = self.RUN_SPEED_PPS * frame_time
        self.move()

    def move(self):
        # dir 이 0 일때는 오른쪽으로 이동
        if self.dir == 0:
          self.x += self.runspeed
        # dir 이 1일 때는 왼쪽으로 이동
        elif self.dir == 1:
          self.x -= self.runspeed

    def draw(self):
        self.image.clip_draw(self.frame*50, 0, 50, 20, self.x, self.y)

    def get_bb(self):
        return self.x - 25, self.y - 10, self.x + 25, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Attack_effect():
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x = 10
        self.y = 10
        self.frame = 0
        self.total_frames = 0
        if Attack_effect.image is None:
            self.image = load_image("attack_effect.png")

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 37, self.x, self.y)

class Attack_effect2():
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x = 10
        self.y = 10
        self.frame = 0
        self.total_frames = 0
        if Attack_effect.image is None:
            self.image = load_image("attack_effect2.png")

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y)

class Special_attack():
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 3.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    image = None

    def __init__(self):
        self.x = 0
        self.y = 0
        self.frame = 0
        self.total_frames = 0
        if Special_attack.image is None:
            self.image = load_image("special_attack.png")

    def update(self, frame_time):
        self.speed = self.RUN_SPEED_PPS * frame_time
        self.y -= self.speed
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 40, self.x, self.y)

class Special_attack_effect():
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    image = None

    def __init__(self):
        self.x = 0
        self.y = 0
        self.frame = 0
        self.total_frames = 0
        if Special_attack_effect.image is None:
            self.image = load_image("special_attack_effect.png")

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)

    def draw(self):
        self.image.clip_draw(self.frame * 70, 0, 70, 80, self.x, self.y)

    def get_bb(self):
        return self.x - 35, self.y - 40, self.x + 35, self.y + 40
