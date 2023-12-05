from pico2d import *
import game_world
import game_framework
import hero
from back_ground import Back_Ground2, Fog, Back_Forest
from ground import Ground2

HUMAN_HP = 0
MONSTER_HP = 1
MONSTER_ATTACK = 4
BOSS_HP = 2
BODY_DAMAGE = 0.2
SKILL_DAMAGE = 40
SKILL2_DAMAGE = 50
ATTACK_DAMAGE = 100

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Hero2.handle_event(event)

def init():

    global Hero2


    open_canvas(1600, 900)

    back_ground = Back_Forest()
    game_world.add_object(back_ground, 0)

    back_ground2 = [Back_Ground2(i * 220 + 130) for i in range(8)]
    game_world.add_objects(back_ground2, 0)

    back_ground3 = [Ground2(i * 500 + 250) for i in range(4)]
    game_world.add_objects(back_ground3, 0)

    back_ground_effect = Fog()
    game_world.add_object(back_ground_effect, 0)

    Hero2 = hero.Hero()
    game_world.add_object(Hero2, 0)

def update():
    game_world.update()
    game_world.handle_collision()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    close_canvas()
    pass


def pause():
    pass


def resume():
    pass
