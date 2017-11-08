from pico2d import *
import random

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
