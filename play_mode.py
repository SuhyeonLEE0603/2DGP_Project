from pico2d import *
import game_world
import game_framework
from hero import Hero
from burning_city import Burning_city
from monster import Monster


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            hero.handle_event(event)

def init():
    global back_ground
    global hero
    global monster

    back_ground = Burning_city()
    game_world.add_object(back_ground)

    hero = Hero()
    game_world.add_object(hero, 1)

    monster = Monster()
    game_world.add_object(monster, 1)
def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass
