from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, open_canvas, close_canvas
import game_framework
import title_mode


def init():
    global image
    global logo_start_time

    open_canvas()

    logo_start_time = get_time()
    image = load_image('./source/tuk_credit.png')
    pass


def finish():
    close_canvas()
    pass


def update():
    global logo_start_time

    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass


def handle_events():
    pass


def pause():
    pass


def resume():
    pass
