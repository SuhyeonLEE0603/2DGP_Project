from pico2d import load_image



class Hp_bar:
    image = None

    def load_iamges(self):
        if Hp_bar.image == None:
            Hp_bar.image = load_image("./source/Hp_bar.png")

    def __init__(self, object):
        self.hp = 300
        self.frame = 0
        self.object = object
        self.load_iamges()

    def draw(self, x, y):
        if self.object == 0:
            self.back_hp_bar = Hp_bar.image.clip_draw(0, 190, 300, 70, x, y, 200, 60)
            self.hp_bar = Hp_bar.image.clip_draw(0, 480, self.hp, 70, x, y, 200, 60)
        elif self.object == 1:
            self.back_hp_bar = Hp_bar.image.clip_draw(0, 120, 300, 70, x, y, 200, 60)
            self.hp_bar = Hp_bar.image.clip_draw(0, 410, self.hp, 70, x, y, 200, 60)

    def update(self):
        # 충돌 처리되면 hp 감소
        pass
