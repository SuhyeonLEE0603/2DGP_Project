from pico2d import *
from burning_city import Burning_city


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def init():
    global running
    global world
    global back_ground

    running = True
    world = []

    back_ground = Burning_city()
    world.append(back_ground)


def update():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
