import random
import game_framework

from pico2d import *

import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from hp_bar import Hp_bar

# Monster Action Speed
FRAMES_PER_WALK = 3
FRAMES_PER_ATTACK = 3
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

animation_names = ['Walk', 'Attack']


class Attack_BB:
    def __init__(self, x, y, dir):
        self.x, self.y, self.dir = x, y + 50, dir
        self.theta = 1
        self.radius = 3
        self.sound = load_wav('./source/monster1_attack.wav')
        self.sound.set_volume(20)
        self.sound.play()

    def update(self):
        dx = math.cos(math.radians(self.theta)) * self.radius
        dy = math.sin(math.radians(self.theta)) * self.radius
        if self.dir == 1:
            self.x += dx * 2
            self.y -= dy
        else:
            self.x -= dx * 2
            self.y -= dy
        self.theta += 0.8
        if self.y < 190:
            game_world.remove_object(self)

    def draw(self):
        pass

    def get_bb(self):

        return self.x - 100, self.y - 10, self.x + 100, self.y + 80


    def handle_collision(self, group, other):
        if group == 'attack:hero':
            game_world.remove_object(self)
            print('몬스터 공격적중')
        if group == 'monster1_attack:hero_attack':
            game_world.remove_object(self)
            print('몬스터 공격 막음')


class Monster:

    def load_images(self):
        self.images = {}
        for name in animation_names:
            if name == 'Walk':
                self.images[name] = [load_image("./source/Demons/demon_knight/sprite/walking/" + "%d" % i + ".png") for
                                     i in
                                     range(3)]
            elif name == 'Attack':
                self.images[name] = [load_image("./source/Demons/demon_knight/sprite/Attack/" + "%d" % i + ".png") for i
                                     in
                                     range(4)]

    def __init__(self):
        self.x, self.y = random.randint(1600 - 800, 1600), 350
        self.load_images()
        self.frame = 0
        self.attack_frame = 1
        self.dir = random.choice([-1, 1])
        self.size_x, self.size_y = 1400, 1000
        self.collision_cnt = 0
        self.hp = Hp_bar(play_mode.MONSTER_HP)
        self.state = 'Walk'
        self.build_behavior_tree()

    def update(self):
        self.bt.run()
        if self.state == 'Walk':
            self.frame = (self.frame + FRAMES_PER_WALK * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.attack_frame = 1
        else:
            if self.attack_frame < 2.5 and self.attack_frame > 2.47:
                self.attack = Attack_BB(self.x, self.y, self.dir)
                game_world.add_object(self.attack)
                game_world.add_collision_pair('attack:hero', self.attack, None)
                game_world.add_collision_pair('monster1_attack:hero_attack', None, self.attack)
            self.attack_frame = (self.attack_frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        if self.state == 'Walk':
            if self.dir < 0:
                self.images[self.state][int(self.frame)].draw(self.x, self.y, self.size_x, self.size_y)
            else:
                self.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size_x,
                                                                        self.size_y)
        else:
            if self.dir < 0:
                self.images[self.state][int(self.attack_frame)].draw(self.x, self.y, self.size_x, self.size_y)
            else:
                self.images[self.state][int(self.attack_frame)].composite_draw(0, 'h', self.x, self.y, self.size_x,
                                                                               self.size_y)
        draw_rectangle(*self.get_bb())
        self.hp.draw(self.x + 150, self.y + 150)

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 100, self.y - 300, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'hero:monster':
            return
        if group == 'fire:monster':
            self.hp.update(play_mode.SKILL_DAMAGE)
        if group == 'attack:monster':
            self.hp.update(play_mode.ATTACK_DAMAGE)
        if group == 'skill2:monster':
            self.hp.update(play_mode.SKILL2_DAMAGE)
        if self.hp.monster_hp <= 0:
            game_world.remove_object(self)
            print('몬스터 삭제')

    def move_range(self):
        self.state = 'Walk'
        if self.x > 1600:
            self.dir = -1
        elif self.x < 700:
            self.dir = 1
        self.x = clamp(700, self.x, 1600)
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (r * PIXEL_PER_METER) ** 2

    def move_slightly_to(self, tx):
        if tx - self.x < 0:
            self.dir = -1
        else:
            self.dir = 1
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time

    def is_hero_nearby(self, r):
        if self.distance_less_than(play_mode.Hero1.x, play_mode.Hero1.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_hero(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.Hero1.x)
        if self.distance_less_than(play_mode.Hero1.x, play_mode.Hero1.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def attack_hero(self):
        self.state = 'Attack'
        if play_mode.Hero1.x < self.x:
            self.dir = -1
        else:
            self.dir = 1

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        a3 = Action('움직이는 범위', self.move_range)

        SEQ_move_left_right = Sequence('좌우 이동', a3)

        c1 = Condition('주인공이 근처에 있는가?', self.is_hero_nearby, 25)
        a4 = Action('주인공으로 이동', self.move_to_hero, 15)
        a5 = Action('가까워 지면 주인공 공격', self.attack_hero)

        SEQ_chase_hero = Sequence('주인공을 추적 후 공격', c1, a4, a5)

        root = SEL_chase_or_wander = Selector('추적 또는 배회', SEQ_chase_hero, SEQ_move_left_right)

        self.bt = BehaviorTree(root)
