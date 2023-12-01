from pico2d import *
import game_world
import game_framework


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

    # fill here
    def get_bb(self):
        return self.x - 50, self.y - 30, self.x, self.y + 150
