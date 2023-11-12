from pico2d import load_image

class Ground:
    image = None

    def load_iamges(self):
        if Ground.image == None:
            Ground.image = load_image("./source/Background/dead_village/ground.png")

    def __init__(self, x=40, y=40):
        self.frame = 0
        self.x = x
        self.y = y
        self.load_iamges()

    def draw(self):
        Ground.image.draw(self.x, self.y)

    def update(self):
        pass
