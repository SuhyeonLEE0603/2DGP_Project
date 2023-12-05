import random
import game_framework

from pico2d import *

import game_world
import play_mode
import play_mode2
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from hp_bar import Hp_bar

# Monster Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Monster Action Speed
FRAMES_PER_WALK = 3
FRAMES_PER_ATTACK = 2
FRAMES_PER_SKILL = 2
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
SKILL_SPEED_KMPH = 20.0  # Km / Hour
SKILL_SPEED_MPM = (SKILL_SPEED_KMPH * 1000.0 / 60.0)
SKILL_SPEED_MPS = (SKILL_SPEED_MPM / 60.0)
SKILL_SPEED_PPS = (SKILL_SPEED_MPS * PIXEL_PER_METER)



animation_names = ['Walk', 'Attack', 'Skill']


class Attack_BB:
    image = None
    def __init__(self):
        if Attack_BB.image == None:
            self.image = load_image("./source/Demons/demon_monk/sprite/attack/attack.gif")

        self.x, self.y,  = play_mode2.Hero2.x, play_mode2.Hero2.y + 350

    def update(self):
        self.y -= SKILL_SPEED_PPS * game_framework.frame_time


    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달
        pass

    def get_bb(self):
        return self.x - 120, self.y - 100, self.x + 100, self.y + 70

    def handle_collision(self, group, other):
        if group == 'attack:hero':
            game_world.remove_object(self)
            print('몬스터 공격적중')
        if group == 'monster_attack:hero_attack':
            game_world.remove_object(self)
            print('몬스터 공격 막음')


class Skill_BB:
    image = None
    def __init__(self, x, y, dir):
        if Skill_BB.image == None:
            self.image = load_image("./source/Demons/demon_monk/sprite/skill/skill.gif")

        self.x, self.y, self.dir = x, y - 100, dir

    def update(self):
        if self.dir == -1:
            self.x -= SKILL_SPEED_PPS * game_framework.frame_time
        else:
            self.x += SKILL_SPEED_PPS * game_framework.frame_time

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달
        pass

    def get_bb(self):
        return self.x - 120, self.y - 100, self.x + 100, self.y + 70

    def handle_collision(self, group, other):
        if group == 'skill:hero':
            game_world.remove_object(self)
            print('몬스터 스킬 적중')
        if group == 'monster_skill:hero_attack':
            game_world.remove_object(self)
            print('몬스터 스킬 막음')



class Monster:

    def load_images(self):
        self.images = {}
        for name in animation_names:
            if name == 'Walk':
                self.images[name] = [load_image("./source/Demons/demon_monk/sprite/walking/" + "%d" % i + ".png") for
                                     i in range(7)]
            elif name == 'Attack':
                self.images[name] = [load_image("./source/Demons/demon_monk/sprite/attack/" + "%d" % i + ".png") for i
                                     in range(3)]
            elif name == 'Skill':
                self.images[name] = [load_image("./source/Demons/demon_monk/sprite/skill/" + "%d" % i + ".png") for i
                                     in range(5)]

    def __init__(self):
        self.x, self.y = 800, 450
        self.load_images()
        self.frame = 0
        self.attack_frame = 0
        self.skill_frame = 0
        self.dir = random.choice([-1, 1])
        self.size_x, self.size_y = 1000, 1000
        self.hp = Hp_bar(play_mode2.MONSTER_HP, 400)
        self.state = 'Walk'
        self.build_behavior_tree()
        self.skill_time = 0
        self.cool_time = False

    def update(self):
        self.bt.run()
        if self.cool_time:
            self.skill_time += game_framework.frame_time
            if self.skill_time > 3:
                self.cool_time = False
                self.skill_time = 0
        if self.state == 'Walk':
            self.frame = (self.frame + FRAMES_PER_WALK * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.attack_frame = 0
            self.skill_frame = 0
        elif self.state == 'Attack':
            if self.attack_frame < 2.5 and self.attack_frame > 2.485:
                self.attack = Attack_BB()
                game_world.add_collision_pair('attack:hero', self.attack, None)
                game_world.add_collision_pair('monster_attack:hero_attack', None, self.attack)
                game_world.add_object(self.attack)
            self.attack_frame = (self.attack_frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 3
        else:
            if self.skill_frame < 4.6 and self.skill_frame > 4.585:
                self.cool_time = True
                self.skill = Skill_BB(self.x, self.y, self.dir)
                game_world.add_collision_pair('skill:hero', self.skill, None)
                game_world.add_collision_pair('monster_skill:hero_attack', None, self.skill)
                game_world.add_object(self.skill)
            self.skill_frame = (self.skill_frame + FRAMES_PER_SKILL * ACTION_PER_TIME * game_framework.frame_time) % 5


    def draw(self):
        if self.state == 'Walk':
            if self.dir < 0:
                self.images[self.state][int(self.frame)].draw(self.x, self.y, self.size_x, self.size_y)
            else:
                self.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size_x, self.size_y)
        elif self.state == 'Attack':
            if self.dir < 0:
                self.images[self.state][int(self.attack_frame)].draw(self.x, self.y, self.size_x, self.size_y)
            else:
                self.images[self.state][int(self.attack_frame)].composite_draw(0, 'h', self.x, self.y, self.size_x, self.size_y)
        else:
            if self.dir < 0:
                self.images[self.state][int(self.skill_frame)].draw(self.x, self.y, self.size_x, self.size_y)
            else:
                self.images[self.state][int(self.skill_frame)].composite_draw(0, 'h', self.x, self.y, self.size_x, self.size_y)
        draw_rectangle(*self.get_bb())
        self.hp.draw(self.x + 150, self.y + 50)

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 70, self.y - 350, self.x + 70, self.y - 30

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
        if self.distance_less_than(play_mode2.Hero2.x, play_mode2.Hero2.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_hero(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode2.Hero2.x)
        if self.distance_less_than(play_mode2.Hero2.x, play_mode2.Hero2.y, self.x, self.y, r):

            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def attack_hero(self):
        if self.cool_time:
            self.state = 'Attack'
        else:
            self.state = 'Skill'

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        a3 = Action('움직이는 범위', self.move_range)

        SEQ_move_left_right = Sequence('좌우 이동', a3)

        c1 = Condition('주인공이 근처에 있는가?', self.is_hero_nearby, 17)
        a4 = Action('주인공으로 이동', self.move_to_hero, 17)
        a5 = Action('가까워 지면 주인공 공격', self.attack_hero)

        SEQ_chase_hero = Sequence('주인공을 추적 후 공격', c1, a4, a5)

        root = SEL_chase_or_wander = Selector('추적 또는 배회', SEQ_chase_hero, SEQ_move_left_right)

        self.bt = BehaviorTree(root)
