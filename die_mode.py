from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, open_canvas, close_canvas, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_r, SDLK_ESCAPE, SDL_QUIT

import game_framework
import play_mode

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_r:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_QUIT:
            game_framework.quit()

def init():
    global image
    global end_start_time

    open_canvas(1200, 740)

    sound = load_wav('./source/game_over.wav')
    sound.set_volume(20)
    sound.play()

    end_start_time = get_time()
    image = load_image('./source/you_die.png')
    pass


def finish():
    close_canvas()
    pass


def update():
    global end_start_time

    if get_time() - end_start_time >= 6.0:
        end_start_time = get_time()
        game_framework.quit()
    pass


def draw():
    clear_canvas()
    image.draw(600, 370)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
