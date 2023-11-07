from pico2d import load_image
import game_framework

# burning city action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7.0


class Burning_city:
    images = None

    def load_iamges(self):
        if Burning_city.images == None:
            Burning_city.images = [load_image("./source/Background/burning_city/" + "%d" % i + ".png") for i in
                                   range(0, 7)]

    def __init__(self, x=400, y=220):
        self.frame = 0
        self.x = x
        self.y = y
        self.load_iamges()

    def draw(self):
        Burning_city.images[int(self.frame)].draw(self.x, self.y, 2400, 1360)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass
