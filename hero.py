from pico2d import load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle
import math

from sdl2 import SDLK_a, SDLK_s, SDLK_d

import die_mode
import play_mode
import skill
import game_world
import game_framework
from hp_bar import Hp_bar
from skill2_icon import Skill2Icon
from skill_icon import SkillIcon


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def skill_over(e):
    return e[0] == 'SKILL_OVER'


def attack_over(e):
    return e[0] == 'ATTACK_OVER'


# Hero Run Speed
PIXEL_PER_METER = (10.0 / 0.15)  # 10 pixel 15 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Hero Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_WALK = 5
FRAMES_PER_ATTACK = 5
FRAMES_PER_SKILL = 5
FRAMES_PER_SKILL2 = 5


class Attack:

    @staticmethod
    def enter(hero, e):
        global attack_bb

        attack_bb = skill.Attack_BB(hero.x, hero.y, hero.face_dir)
        game_world.add_object(attack_bb)
        game_world.add_collision_pair('attack:monster', attack_bb, None)
        game_world.add_collision_pair('monster2_attack:hero_attack', attack_bb, None)
        game_world.add_collision_pair('monster1_attack:hero_attack', attack_bb, None)
        game_world.add_collision_pair('monster_skill:hero_attack', attack_bb, None)
        pass

    @staticmethod
    def exit(hero, e):
        if attack_bb in game_world.objects[0]:
            game_world.remove_object(attack_bb)
        hero.attack_frame = 0
        hero.state_machine.prev_state = Attack
        pass

    @staticmethod
    def do(hero):
        hero.attack_frame = (hero.attack_frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 3
        if hero.attack_frame > 2.9:
            hero.state_machine.handle_event(('ATTACK_OVER', 0))

    @staticmethod
    def draw(hero):
        if hero.face_dir == -1:
            hero.AttackImage[int(hero.attack_frame)].draw(hero.x + 10, hero.y + 75)
        else:
            hero.AttackImage[int(hero.attack_frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)
class RightAttack:

    @staticmethod
    def enter(hero, e):
        global attack_bb

        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            hero.dir, hero.face_dir = 1, 1
        attack_bb = skill.Attack_BB(hero.x, hero.y, hero.face_dir)
        game_world.add_object(attack_bb)
        game_world.add_collision_pair('attack:monster', attack_bb, None)
        game_world.add_collision_pair('monster2_attack:hero_attack', attack_bb, None)
        game_world.add_collision_pair('monster1_attack:hero_attack', attack_bb, None)
        game_world.add_collision_pair('monster_skill:hero_attack', attack_bb, None)
        pass

    @staticmethod
    def exit(hero, e):
        if attack_bb in game_world.objects[0]:
            game_world.remove_object(attack_bb)
        hero.attack_frame = 0
        hero.state_machine.prev_state = Attack
        pass

    @staticmethod
    def do(hero):
        hero.attack_frame = (hero.attack_frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 3
        if hero.attack_frame > 2.9:
            hero.state_machine.handle_event(('ATTACK_OVER', 0))

    @staticmethod
    def draw(hero):
        hero.AttackImage[int(hero.attack_frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)

class LeftAttack:

    @staticmethod
    def enter(hero, e):
        global attack_bb

        if left_down(e) or right_up(e):  # 왼쪽으로 RUN
            hero.dir, hero.face_dir = -1, -1
        attack_bb = skill.Attack_BB(hero.x, hero.y, hero.face_dir)
        game_world.add_object(attack_bb)
        game_world.add_collision_pair('attack:monster', attack_bb, None)
        game_world.add_collision_pair('monster2_attack:hero_attack', attack_bb, None)
        game_world.add_collision_pair('monster1_attack:hero_attack', attack_bb, None)
        game_world.add_collision_pair('monster_skill:hero_attack', attack_bb, None)
        pass

    @staticmethod
    def exit(hero, e):
        if attack_bb in game_world.objects[0]:
            game_world.remove_object(attack_bb)
        hero.attack_frame = 0
        hero.state_machine.prev_state = Attack
        pass

    @staticmethod
    def do(hero):
        hero.attack_frame = (hero.attack_frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 3
        if hero.attack_frame > 2.9:
            hero.state_machine.handle_event(('ATTACK_OVER', 0))

    @staticmethod
    def draw(hero):
        hero.AttackImage[int(hero.attack_frame)].draw(hero.x + 10, hero.y + 75)


class Skill2:

    @staticmethod
    def enter(hero, e):
        global skill2_bb

        if hero.skill_icon2.run:
            print('스킬2 쿨타임')
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        else:
            skill2_bb = skill.Skill2_BB(hero.x, hero.y, hero.face_dir)
            game_world.add_object(skill2_bb)
            game_world.add_collision_pair('skill2:monster', skill2_bb, None)


    @staticmethod
    def exit(hero, e):
        if skill2_bb in game_world.objects[0]:
            game_world.remove_object(skill2_bb)
        hero.skill_frame = 0
        hero.state_machine.prev_state = Skill
        hero.skill_icon2.run_cool_time()
        pass

    @staticmethod
    def do(hero):
        hero.skill_frame = (hero.skill_frame + FRAMES_PER_SKILL2 * ACTION_PER_TIME * game_framework.frame_time)
        if hero.skill_frame > 7:
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        pass

    @staticmethod
    def draw(hero):
        if hero.face_dir == -1:
            hero.Skill2Image[int(hero.skill_frame)].draw(hero.x + 10, hero.y + 75)
        else:
            hero.Skill2Image[int(hero.skill_frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)
        pass



class RightSkill2:

    @staticmethod
    def enter(hero, e):
        global skill2_bb

        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            hero.dir, hero.face_dir = 1, 1
        if hero.skill_icon2.run:
            print('스킬2 쿨타임')
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        else:
            skill2_bb = skill.Skill2_BB(hero.x, hero.y, hero.face_dir)
            game_world.add_object(skill2_bb)
            game_world.add_collision_pair('skill2:monster', skill2_bb, None)


    @staticmethod
    def exit(hero, e):
        if skill2_bb in game_world.objects[0]:
            game_world.remove_object(skill2_bb)
        hero.skill_frame = 0
        hero.state_machine.prev_state = Skill
        hero.skill_icon2.run_cool_time()
        pass

    @staticmethod
    def do(hero):
        hero.skill_frame = (hero.skill_frame + FRAMES_PER_SKILL2 * ACTION_PER_TIME * game_framework.frame_time)
        if hero.skill_frame > 7:
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.Skill2Image[int(hero.skill_frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)



class LeftSkill2:

    @staticmethod
    def enter(hero, e):
        global skill2_bb

        if left_down(e) or right_up(e):  # 왼쪽으로 RUN
            hero.dir, hero.face_dir = -1, -1
        if hero.skill_icon2.run:
            print('스킬2 쿨타임')
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        else:
            skill2_bb = skill.Skill2_BB(hero.x, hero.y, hero.face_dir)
            game_world.add_object(skill2_bb)
            game_world.add_collision_pair('skill2:monster', skill2_bb, None)


    @staticmethod
    def exit(hero, e):
        if skill2_bb in game_world.objects[0]:
            game_world.remove_object(skill2_bb)
        hero.skill_frame = 0
        hero.state_machine.prev_state = Skill
        hero.skill_icon2.run_cool_time()
        pass

    @staticmethod
    def do(hero):
        hero.skill_frame = (hero.skill_frame + FRAMES_PER_SKILL2 * ACTION_PER_TIME * game_framework.frame_time)
        if hero.skill_frame > 7:
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.Skill2Image[int(hero.skill_frame)].draw(hero.x + 10, hero.y + 75)


class LeftSkill:

    @staticmethod
    def enter(hero, e):
        if left_down(e) or right_up(e):  # 왼쪽으로 RUN
            hero.dir, hero.face_dir = -1, -1
        if hero.skill_icon1.run:
            print('스킬1 쿨타임')
            hero.state_machine.handle_event(('SKILL_OVER', 0))

    @staticmethod
    def exit(hero, e):
        hero.skill_frame = 0
        hero.fire()
        pass

    @staticmethod
    def do(hero):
        hero.skill_frame = (hero.skill_frame + FRAMES_PER_SKILL * ACTION_PER_TIME * game_framework.frame_time) % 5
        if hero.skill_frame > 4.9:
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.SkillImage[int(hero.skill_frame)].draw(hero.x + 10, hero.y + 75)

class RightSkill:

    @staticmethod
    def enter(hero, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            hero.dir, hero.face_dir = 1, 1
        if hero.skill_icon1.run:
            print('스킬1 쿨타임')
            hero.state_machine.handle_event(('SKILL_OVER', 0))

    @staticmethod
    def exit(hero, e):
        hero.skill_frame = 0
        hero.fire()
        pass

    @staticmethod
    def do(hero):
        hero.skill_frame = (hero.skill_frame + FRAMES_PER_SKILL * ACTION_PER_TIME * game_framework.frame_time) % 5
        if hero.skill_frame > 4.9:
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.SkillImage[int(hero.skill_frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)


class Skill:

    @staticmethod
    def enter(hero, e):
        if hero.skill_icon1.run:
            print('스킬1 쿨타임')
            hero.state_machine.handle_event(('SKILL_OVER', 0))

    @staticmethod
    def exit(hero, e):
        hero.skill_frame = 0
        hero.fire()
        pass

    @staticmethod
    def do(hero):
        hero.skill_frame = (hero.skill_frame + FRAMES_PER_SKILL * ACTION_PER_TIME * game_framework.frame_time) % 5
        if hero.skill_frame > 4.9:
            hero.state_machine.handle_event(('SKILL_OVER', 0))
        pass

    @staticmethod
    def draw(hero):
        if hero.face_dir == -1:
            hero.SkillImage[int(hero.skill_frame)].draw(hero.x + 10, hero.y + 75)
        else:
            hero.SkillImage[int(hero.skill_frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)
        pass


class Stand:

    @staticmethod
    def enter(hero, e):
        pass

    @staticmethod
    def exit(hero, e):
        hero.state_machine.prev_state = Stand
        pass

    @staticmethod
    def do(hero):
        pass

    @staticmethod
    def draw(hero):
        if hero.face_dir == -1:
            hero.images.draw(hero.x, hero.y)
        else:
            hero.images.composite_draw(math.radians(180), 'v', hero.x, hero.y)
        pass


class LeftWalk:

    @staticmethod
    def enter(hero, e):
        hero.state_machine.prev_state = LeftWalk
        if left_down(e) or right_up(e):  # 왼쪽으로 RUN
            hero.dir, hero.face_dir = -1, -1

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        hero.x = clamp(25, hero.x, 1600 - 25)
        hero.frame = (hero.frame + FRAMES_PER_WALK * ACTION_PER_TIME * game_framework.frame_time) % 5

    @staticmethod
    def draw(hero):
        if hero.dir == -1:
            hero.WalkingImage[int(hero.frame)].draw(hero.x, hero.y + 75)


class RightWalk:

    @staticmethod
    def enter(hero, e):
        hero.state_machine.prev_state = RightWalk
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            hero.dir, hero.face_dir = 1, 1

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        hero.x = clamp(25, hero.x, 1600 - 25)
        hero.frame = (hero.frame + FRAMES_PER_WALK * ACTION_PER_TIME * game_framework.frame_time) % 5

    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.WalkingImage[int(hero.frame)].composite_draw(math.radians(180), 'v', hero.x, hero.y + 75)


class StateMachine:
    def __init__(self, hero):
        self.hero = hero
        self.cur_state = Stand
        self.perv_state = None
        self.transitations = {
            Stand: {right_down: RightWalk, left_down: LeftWalk, left_up: RightWalk, right_up: LeftWalk, a_down: Attack,
                    s_down: Skill, d_down: Skill2},
            LeftWalk: {right_down: Stand, left_up: Stand, a_down: LeftAttack, s_down: LeftSkill, d_down: LeftSkill2},
            RightWalk: {left_down: Stand, right_up: Stand, a_down: RightAttack, s_down: RightSkill, d_down: RightSkill2},
            Attack: {right_down: RightWalk, left_down: LeftWalk, attack_over: Stand, a_up: Stand},
            LeftAttack: {left_up: Stand, attack_over: LeftWalk, right_down: RightWalk, s_down: LeftSkill, d_down: LeftSkill2},
            RightAttack: {right_up: Stand, attack_over: RightWalk, left_down: LeftWalk, s_down: RightSkill, d_down: RightSkill2},
            Skill: {right_down: RightWalk, left_down: LeftWalk, right_up: LeftWalk, left_up: RightWalk, skill_over: Stand},
            LeftSkill: {left_up: Stand, skill_over: LeftWalk, right_down: RightWalk, a_down: LeftAttack, d_down: LeftSkill2},
            RightSkill: {right_up: Stand, skill_over: RightWalk, left_down: LeftWalk, a_down: RightAttack, d_down: RightSkill2},
            Skill2: {right_down: RightWalk, left_down: LeftWalk,right_up: LeftWalk, left_up: RightWalk, skill_over: Stand},
            RightSkill2: {right_up: Stand, skill_over: RightWalk, left_down: LeftWalk, a_down: RightAttack, s_down: RightSkill},
            LeftSkill2: {left_up: Stand, skill_over: LeftWalk, right_down: RightWalk, a_down: LeftAttack, s_down: LeftSkill}
        }

    def start(self):
        self.cur_state.enter(self.hero, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hero)

    def handle_event(self, e):
        for check_event, next_state in self.transitations[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hero, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hero, e)
                return True

    def draw(self):
        self.cur_state.draw(self.hero)


class Hero:

    def load_images(self):

        self.images = load_image('./source/Humans/Knight1/0.png')
        self.WalkingImage = [load_image("./source/Humans/Knight1/sprite/walking/" + "%d" % i + ".png") for i in
                             range(5)]
        self.AttackImage = [load_image("./source/Humans/Knight1/sprite/attack/" + "%d" % i + ".png") for i in
                            range(3)]
        self.SkillImage = [load_image("./source/Humans/Knight1/sprite/attack1/" + "%d" % i + ".png") for i in
                           range(5)]
        self.Skill2Image = [load_image("./source/Humans/Knight1/sprite/attack2/" + "%d" % i + ".png") for i in
                            range(7)]

    def __init__(self):
        self.x, self.y = 100, 180
        self.frame = 0
        self.attack_frame = 0
        self.skill_frame = 0
        self.face_dir = 1
        self.dir = 0
        self.jump_time = 0
        self.jump_speed = 7
        self.hp = Hp_bar(play_mode.HUMAN_HP)
        self.skill_icon1 = SkillIcon()
        self.skill_icon2 = Skill2Icon()
        self.load_images()
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def fire(self):
        if self.skill_icon1.run:
            print('스킬1 쿨타임')
        else:
            fire = skill.Skill(self.x, self.y + 100, 40, self.face_dir)
            game_world.add_object(fire)
            self.skill_icon1.run_cool_time()
            game_world.add_collision_pair('fire:monster', fire, None)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.skill_icon1.update()
        self.skill_icon2.update()
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        self.hp.draw(self.x + 110, self.y + 200)
        self.skill_icon1.draw(self.x - 100, self.y)
        self.skill_icon2.draw(self.x - 50, self.y)
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달

    def get_bb(self):
        return self.x - 35, self.y - 100, self.x + 35, self.y + 100  # 값 4개 짜리 튜플 1개

    def handle_collision(self, group, other):
        if group == 'hero:monster':
            print('데미지 입음')
            self.hp.update(play_mode.BODY_DAMAGE)
        if group == 'attack:hero':
            print('데미지 입음')
            self.hp.update(play_mode.MONSTER_ATTACK)
        if group == 'skill:hero':
            print('데미지 입음')
            self.hp.update(play_mode.MONSTER_SKILL)
        if self.hp.hero_hp <= 0:
            game_framework.change_mode(die_mode)