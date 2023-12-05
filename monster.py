import random
import math
import game_framework

from pico2d import *

import game_world
import play_mode
from hp_bar import Hp_bar

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_WALKING = 3.0

animation_names = ['Walk']


class Monster:


    def load_images(self):
        self.images = load_image('./source/Humans/Knight1/0.png')
        self.WalkingImage = [load_image("./source/Demons/demon_knight/sprite/walking/" + "%d" % i + ".png") for i in
                             range(3)]
        self.AttackImage = [load_image("./source/Demons/demon_knight/sprite/Attack/" + "%d" % i + ".png") for i in
                            range(4)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 400
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1, 1])
        self.size_x, self.size_y = 1400, 1000
        self.collision_cnt = 0
        self.hp = Hp_bar(play_mode.MONSTER_HP)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_WALKING * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_WALKING
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass

    def draw(self):
        if self.dir > 0:
            self.WalkingImage[int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size_x, self.size_y)
        else:
            self.WalkingImage[int(self.frame)].draw(self.x, self.y, self.size_x, self.size_y)
        draw_rectangle(*self.get_bb())
        self.hp.draw(self.x + 150, self.y + 150)

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 100, self.y - 300, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'hero:monster':
            pass
        if group == 'fire:monster':
            if self.hp.monster_hp < 0:
                game_world.remove_object(self)
                print('몬스터 삭제')
                return
            self.hp.update(play_mode.SKILL_DAMAGE)
            print('몬스터 데미지 입음')
        if group == 'attack:monster':
            self.hp.update(play_mode.ATTACK_DAMAGE)
            print('몬스터 데미지 입음')
        if group == 'skill2:monster':
            self.hp.update(play_mode.SKILL2_DAMAGE)
            pass
