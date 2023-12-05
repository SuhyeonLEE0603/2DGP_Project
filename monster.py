import random
import game_framework

from pico2d import *

import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from hp_bar import Hp_bar

# Monster Action Speed
FRAMES_PER_WALK = 3
FRAMES_PER_ATTACK = 2
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
        self.x, self.y, self.dir = x, y, dir
        self.theta = 1
        self.radius = 3  # 원운동 반지름

    def update(self):
        dx = math.cos(math.radians(self.theta)) * self.radius
        dy = math.sin(math.radians(self.theta)) * self.radius
        if self.dir == 1:
            self.x += dx
            self.y -= dy
        else:
            self.x -= dx
            self.y -= dy
        self.theta += 1
        if self.y <= self.x:
            game_world.remove_object(self)
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달
        pass

    def get_bb(self):
        return self.x - 30, self.y + 200, self.x + 25, self.y + 300

    def handle_collision(self, group, other):
        if group == 'attack:hero':
            print('공격적중')
            game_world.remove_object(self)
            pass


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
        self.x, self.y = random.randint(1600 - 800, 1600), 400
        self.load_images()
        self.frame = random.randint(0, 9)
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
        else:
            self.frame = (self.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 4
        # self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        # if self.x > 1600:
        #     self.dir = -1
        # elif self.x < 800:
        #     self.dir = 1
        # self.x = clamp(800, self.x, 1600)

    def draw(self):
        if self.dir < 0:
            self.images[self.state][int(self.frame)].draw(self.x, self.y, self.size_x, self.size_y)
        else:
            self.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size_x, self.size_y)

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
            self.hp.update(play_mode.SKILL_DAMAGE)
            if self.hp.monster_hp < 0:
                game_world.remove_object(self)
                print('몬스터 삭제')
                return
        if group == 'attack:monster':
            self.hp.update(play_mode.ATTACK_DAMAGE)
            if self.hp.monster_hp < 0:
                game_world.remove_object(self)
                print('몬스터 삭제')
                return
        if group == 'skill2:monster':
            self.hp.update(play_mode.SKILL2_DAMAGE)
            if self.hp.monster_hp < 0:
                game_world.remove_object(self)
                print('몬스터 삭제')
                return
            pass
    def move_range(self):
        self.state = 'Walk'
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
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
        if self.distance_less_than(play_mode.hero.x, play_mode.hero.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_hero(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.hero.x)
        if self.distance_less_than(play_mode.hero.x, play_mode.hero.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def attack_hero(self, r):
        self.state = 'Attack'
        attack = Attack_BB(self.x, self.y, self.dir)
        game_world.add_object(attack)
        game_world.add_collision_pair('attack:hero', attack, None)
        if self.distance_less_than(play_mode.hero.x, play_mode.hero.y, self.x, self.y, r):
            return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a3 = Action('움직이는 범위', self.move_range)

        SEQ_move_left_right = Sequence('좌우 이동', a3)

        c1 = Condition('주인공이 근처에 있는가?', self.is_hero_nearby, 15)
        a4 = Action('주인공으로 이동', self.move_to_hero, 15)
        a5 = Action('가까워 지면 주인공 공격', self.attack_hero, 15)

        SEQ_chase_hero = Sequence('주인공을 추적 후 공격', c1, a4, a5)

        root = SEL_chase_or_wander = Selector('추적 또는 배회', SEQ_chase_hero, SEQ_move_left_right)

        self.bt = BehaviorTree(root)
