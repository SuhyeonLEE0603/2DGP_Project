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
        self.radius = 2.5  # 원운동 반지름

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
        self.theta += 1

    def draw(self):
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달
        pass

    def get_bb(self):
        return self.x - 30, self.y + 100, self.x + 25, self.y + 150

    def handle_collision(self, group, other):
        if group == 'attack:monster':
            print('공격적중')
            game_world.remove_object(self)
            pass


class Skill:
    image = None

    def __init__(self, x=400, y=300, velocity=1, dir=1):
        if Skill.image == None:
            Skill.image = load_image(f"./source/Humans/Knight1/sprite/attack1/Skill1.png")
        self.x, self.y, self.velocity = x, y, velocity
        self.dir = dir

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())  # 튜플을 풀어헤쳐서 각각 인자로 전달

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
