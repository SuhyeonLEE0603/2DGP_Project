from pico2d import *

import end_mode
import game_world
import game_framework
import hero
import monster2
from back_ground import Back_Ground2, Fog, Back_Forest
from ground import Ground2

HUMAN_HP = 0
MONSTER_HP = 1
MONSTER_ATTACK = 4
BOSS_HP = 2
BODY_DAMAGE = 0.2
SKILL_DAMAGE = 40
SKILL2_DAMAGE = 50
ATTACK_DAMAGE = 10
MONSTER_SKILL = 30

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
    global Monster2
    global play_mode2_sound

    open_canvas(1600, 900)
    play_mode2_sound = load_wav('./source/play_mode2.wav')
    play_mode2_sound.repeat_play()

    back_ground = Back_Forest()
    game_world.add_object(back_ground, 0)

    back_ground2 = [Back_Ground2(i * 220 + 130) for i in range(8)]
    game_world.add_objects(back_ground2, 0)

    back_ground3 = [Ground2(i * 500 + 250) for i in range(4)]
    game_world.add_objects(back_ground3, 0)

    back_ground_effect = Fog()
    game_world.add_object(back_ground_effect, 0)

    Hero2 = hero.Hero()
    game_world.add_object(Hero2, 1)
    game_world.add_collision_pair('hero:monster', Hero2, None)
    game_world.add_collision_pair('attack:hero', None, Hero2)
    game_world.add_collision_pair('skill:hero', None, Hero2)

    Monster2 = monster2.Monster()
    game_world.add_object(Monster2, 1)
    game_world.add_collision_pair('hero:monster', None, Monster2)
    game_world.add_collision_pair('fire:monster', None, Monster2)
    game_world.add_collision_pair('attack:monster', None, Monster2)
    game_world.add_collision_pair('skill2:monster', None, Monster2)

def update():
    global  Hero2

    if (Hero2.x > 1500) and (Monster2 not in game_world.objects[1]):
        game_framework.change_mode(end_mode)
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
