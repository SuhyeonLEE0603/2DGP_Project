from pico2d import load_image

import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7.0

class Back_Forest:

    def load_iamges(self):

        Back_Forest.image = load_image("./source/Background/forest/back.png")

    def __init__(self, x=800, y=450):
        self.frame = 0
        self.x = x
        self.y = y
        self.load_iamges()

    def draw(self):
        Back_Forest.image.draw(self.x, self.y)

    def update(self):
        pass

class Back_Ground2:

    def load_iamges(self):

        Back_Ground2.image = load_image("./source/Background/forest/platform2.png")

    def __init__(self, x=130, y=150):
        self.frame = 0
        self.x = x
        self.y = y
        self.load_iamges()

    def draw(self):
        Back_Ground2.image.draw(self.x, self.y, 300, 1500)

    def update(self):
        pass


class Fog:

    def load_iamges(self):
        self.images = [load_image("./source/Environmental_Effect/fog_1/" + "%d" % i + ".png") for i in
                               range(0, 18)]

    def __init__(self, x=400, y=220):
        self.frame = 0
        self.x = x
        self.y = y
        self.load_iamges()

    def draw(self):
        self.images[int(self.frame)].draw(self.x, self.y, 2400, 1360)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass

