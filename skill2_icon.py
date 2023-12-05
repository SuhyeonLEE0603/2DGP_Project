from pico2d import *
import game_framework


class Skill2Icon:

    def __init__(self):

        self.image = load_image(f"./source/Humans/Knight1/sprite/attack2/Skill_Icon2.png")
        self.font = load_font('ENCR10B.TTF', 16)
        self.cool_time = 7
        self.run = False

    def draw(self, x, y):
        self.image.draw(x, y + 260, 40, 40)
        if self.run:
            self.font.draw(x - 19, y + 290, f'{self.cool_time:0.2f}', (255, 255, 0))

    def update(self):
        if self.run:
            self.cool_time -= game_framework.frame_time
            if self.cool_time < 0:
                self.cool_time = 7
                self.run = False

    def run_cool_time(self):
        self.run = True     # 쿨타임 활성화

