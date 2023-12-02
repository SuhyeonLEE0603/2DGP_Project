from pico2d import load_image



class Hp_bar:
    image = None

    def load_iamges(self):
        if Hp_bar.image == None:
            Hp_bar.image = load_image("./source/Hp_bar.png")

    def __init__(self, object):
        self.hero_hp = 100
        self.monster_hp = 700
        self.frame = 0
        self.object = object
        self.load_iamges()

    def draw(self, x, y):
        if self.object == 0:
            self.back_hp_bar = Hp_bar.image.clip_draw(0, 190, 500, 70, x, y)
            self.hp_bar = Hp_bar.image.clip_draw(0, 480, self.hero_hp, 70, x, y)
        elif self.object == 1:
            self.back_hp_bar = Hp_bar.image.clip_draw(0, 520, 500, 70, x, y, 200, 60)
            self.hp_bar = Hp_bar.image.clip_draw(0, 410, self.monster_hp, 70, x, y, 200, 60)

    def update(self, hp):
        if self.object == 0:
            self.hero_hp -= hp
        elif self.object == 1:
            self.monster_hp -= hp
        pass
