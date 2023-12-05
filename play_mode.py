from pico2d import *
import game_world
import game_framework
from ground import Ground
from hero import Hero
from burning_city import Burning_city
from monster import Monster
from skill_icon import SkillIcon

HUMAN_HP = 0
MONSTER_HP = 1
BOSS_HP = 2
BODY_DAMAGE = 1
SKILL_DAMAGE = 10
ATTACK_DAMAGE = 1

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            hero.handle_event(event)

def init():
    global hero
    global monster


    open_canvas(1600, 900)

    back_ground = Burning_city()
    game_world.add_object(back_ground, 0)

    hero = Hero()
    game_world.add_object(hero, 2)
    game_world.add_collision_pair('hero:monster', hero, None)

    monster = Monster()
    game_world.add_object(monster, 1)
    game_world.add_collision_pair('hero:monster', None, monster)
    game_world.add_collision_pair('fire:monster', None, monster)
    game_world.add_collision_pair('attack:monster', None, monster)

    grounds = [Ground(i * 200 + 100) for i in range(8)]
    game_world.add_objects(grounds, 0)

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
