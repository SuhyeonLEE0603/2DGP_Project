from pico2d import *
import game_world
import game_framework
import play_mode2
from ground import Ground
import hero
from burning_city import Burning_city
from monster import Monster

HUMAN_HP = 0
MONSTER_HP = 1
MONSTER_ATTACK = 10
BOSS_HP = 2
BODY_DAMAGE = 0.1
SKILL_DAMAGE = 60
SKILL2_DAMAGE = 70
ATTACK_DAMAGE = 10
MONSTER_SKILL = 70

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Hero1.handle_event(event)

def init():
    global Hero1
    global monster
    global back_ground
    global grounds

    open_canvas(1600, 900)

    # sound = load_wav('./source/play_mode1.wav')
    # sound.set_volume(20)
    # sound.play()

    back_ground = Burning_city()
    game_world.add_object(back_ground, 0)

    Hero1 = hero.Hero()
    game_world.add_object(Hero1, 2)
    game_world.add_collision_pair('hero:monster', Hero1, None)
    game_world.add_collision_pair('attack:hero', None, Hero1)

    monster = Monster()
    game_world.add_object(monster, 1)
    game_world.add_collision_pair('hero:monster', None, monster)
    game_world.add_collision_pair('fire:monster', None, monster)
    game_world.add_collision_pair('attack:monster', None, monster)
    game_world.add_collision_pair('skill2:monster', None, monster)

    grounds = [Ground(i * 200 + 100) for i in range(8)]
    game_world.add_objects(grounds, 0)

def update():
    if (monster not in game_world.objects[1]) and (Hero1.x > 1500):
        game_framework.change_mode(play_mode2)
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
