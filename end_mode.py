from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, open_canvas, close_canvas, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework

def init():
    global image
    global ending_start_time
    global end_sound

    open_canvas(790, 600)

    end_sound = load_wav('./source/end_mode.wav')
    # end_sound.set_volume(20)
    end_sound.play()
    ending_start_time = get_time()
    image = load_image('./source/ending.png')
    pass


def finish():

    close_canvas()
    pass


def update():
    global ending_start_time

    if get_time() - ending_start_time >= 5.0:
        ending_start_time = get_time()
        game_framework.quit()
    pass


def draw():
    clear_canvas()
    image.draw(385, 300)
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def pause():
    pass


def resume():
    pass
