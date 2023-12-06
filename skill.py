from pico2d import *
import game_world
import game_framework
import math


class Attack_BB():

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.theta = 1
        self.dir = dir
        self.radius = 2  # 원운동 반지름
        self.attack_sound = load_wav('./source/sword_sound.wav')
        self.attack_sound.set_volume(20)
        self.attack_sound.play()

    def update(self):
        # 공격 BB 회전
        dx = math.cos(math.radians(self.theta)) * self.radius
        dy = math.sin(math.radians(self.theta)) * self.radius
        if self.dir == 1:
            self.x += dx
            self.y -= dy
        else:
            self.x -= dx
            self.y -= dy
        self.theta += 0.7

    def draw(self):
        pass

    def get_bb(self):
        return self.x - 25, self.y + 100, self.x + 25, self.y + 250

    def handle_collision(self, group, other):
        if group == 'attack:monster':
            print('공격적중')
            game_world.remove_object(self)
        if group == 'monster_attack:hero_attack':
            print('공격 막음')
            game_world.remove_object(self)
        if group == 'monster_skill:hero_attack':
            print('공격 막음')
            game_world.remove_object(self)
        if group == 'monster1_attack:hero_attack':
            print('공격 막음')
            game_world.remove_object(self)


class Skill:

    def __init__(self, x=400, y=300, velocity=1, dir=1):

        self.image = load_image(f"./source/Humans/Knight1/sprite/attack1/Skill1.png")
        self.x, self.y, self.velocity = x, y, velocity
        self.dir = dir
        self.sound = load_wav('./source/skill.wav')
        self.sound.set_volume(20)
        self.sound.play()

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        if self.dir == 1:
            self.x += (self.velocity * self.velocity) * game_framework.frame_time
        else:
            self.x += -(self.velocity * self.velocity) * game_framework.frame_time
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'fire:monster':
            print('스킬적중')
            game_world.remove_object(self)
            pass


class Skill2_BB:

    def __init__(self, x, y, dir):
        self.x, self.y = x, y
        self.dir = dir
        self.sound = load_wav('./source/skill2.wav')
        self.sound.set_volume(20)
        self.sound.play()

    def draw(self):
        pass
    def update(self):
        pass

    def get_bb(self):
        if self.dir == 1:
            return self.x + 50, self.y - 100, self.x + 200, self.y - 50
        elif self.dir == -1:
            return self.x - 50, self.y - 100, self.x - 200, self.y - 50

    def handle_collision(self, group, other):
        if group == 'skill2:monster':
            print('스킬2적중')
            game_world.remove_object(self)
            pass
