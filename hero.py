from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle
import math

from sdl2 import SDLK_a, SDLK_s
import skill
import game_world
import game_framework


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

def skill_over(e):
    return e[0] == 'SKILL_OVER'

# Hero Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
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


class Attack:

    @staticmethod
    def enter(hero, e):
        pass

    @staticmethod
    def exit(hero, e):
        hero.state_machine.prev_state = Attack
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 3
        pass

    @staticmethod
    def draw(hero):
        if hero.face_dir == -1:
            hero.AttackImage[int(hero.frame)].draw(hero.x + 10, hero.y + 75)
        else:
            hero.AttackImage[int(hero.frame)].composite_draw(math.radians(180), 'v', hero.x + 10, hero.y + 75)
        pass

class Skill:

    @staticmethod
    def enter(hero, e):
        pass

    @staticmethod
    def exit(hero, e):
        hero.skill_frame = 0
        hero.state_machine.prev_state = Skill
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
        print('Stand Do')
        pass

    @staticmethod
    def draw(hero):
        if hero.face_dir == -1:
            hero.images.draw(hero.x, hero.y)
        else:
            hero.images.composite_draw(math.radians(180), 'v', hero.x, hero.y)
        pass


class Walk:

    @staticmethod
    def enter(hero, e):
        hero.state_machine.prev_state = Walk
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            hero.dir, hero.face_dir = 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            hero.dir, hero.face_dir = -1, -1

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        hero.x = clamp(25, hero.x, 1600 - 25)
        hero.frame = (hero.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 5

    @staticmethod
    def draw(hero):
        if hero.dir == -1:
            hero.WalkingImage[int(hero.frame)].draw(hero.x, hero.y + 75)
        else:
            hero.WalkingImage[int(hero.frame)].composite_draw(math.radians(180), 'v', hero.x, hero.y + 75)


class StateMachine:
    def __init__(self, hero):
        self.hero = hero
        self.cur_state = Stand
        self.perv_state = None
        self.transitions = {
            Stand: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, a_down: Attack, s_down: Skill},
            Walk: {right_down: Stand, left_down: Stand, right_up: Stand, left_up: Stand, space_down: Walk,
                   a_down: Attack, s_down: Skill},
            Attack: {right_down: Walk, left_down: Walk, right_up: Stand, left_up: Stand,
                     a_up: Walk if self.perv_state == Walk else Stand},
            Skill: {right_down: Walk, left_down: Walk, right_up: Walk, left_up: Walk, skill_over: Stand}
        }

    def start(self):
        self.cur_state.enter(self.hero, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hero)

    def handle_event(self, e):
        print('Check Event')
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hero, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hero, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.hero)


class Hero:
    images = None

    def load_images(self):
        if Hero.images == None:
            Hero.images = load_image('./source/Humans/Knight1/0.png')
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
        self.skill_frame = 0
        self.face_dir = 1
        self.dir = 0
        self.load_images()
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def fire(self):
        fire = skill.Skill(self.x, self.y, self.face_dir * 10)
        game_world.add_object(fire)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달

    def get_bb(self):
        return self.x - 35, self.y - 100, self.x + 35, self.y + 100  # 값 4개 짜리 튜플 1개