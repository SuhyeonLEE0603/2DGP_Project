from pico2d import load_image
import os


class Burning_city:

    def __init__(self, x=400, y=300):
        self.t = 0
        self.frame = 0
        self.x = x
        self.y = y
        os.chdir("source/Background/burning_city")

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.image = load_image(f"{self.t}.png")
        self.frame = (self.frame + 1) % 8
        pass
