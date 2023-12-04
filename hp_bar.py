from pico2d import load_image



class Hp_bar:
    image = None

    def load_iamges(self):
        if Hp_bar.image == None:
            Hp_bar.image = load_image("./source/Hp_bar.png")

    def __init__(self, object):
        self.hero_hp = 500
        self.monster_hp = 700
        self.frame = 0
        self.object = object
        self.load_iamges()

    def draw(self, x, y):
        if self.object == 0:
            self.back_hp_bar = Hp_bar.image.clip_draw(0, 190, 500, 90, x, y)
            self.hp_bar = Hp_bar.image.clip_draw(500 - self.hero_hp, 480, 500, 70, x, y)
        elif self.object == 1:
            self.back_hp_bar = Hp_bar.image.clip_draw(0, 120, 700, 75, x, y)
            self.hp_bar = Hp_bar.image.clip_draw(700 - self.monster_hp, 410, 700, 70, x, y)

    def update(self, hp):
        if self.object == 0:
            self.hero_hp -= hp
        elif self.object == 1:
            self.monster_hp -= hp
        pass