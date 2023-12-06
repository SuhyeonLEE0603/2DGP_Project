from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, open_canvas, close_canvas, load_wav, \
    load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode


def init():
    global image
    global title_sound

    open_canvas(1300, 450)

    image = load_image('./source/title.png')
    title_sound = load_wav('./source/title_mode.wav')
    # title_sound.set_volume(20)
    title_sound.repeat_play()

def update():
    pass

def finish():
    close_canvas()
    pass

def draw():
    clear_canvas()
    image.draw(640, 248)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def pause():
    pass


def resume():
    pass
