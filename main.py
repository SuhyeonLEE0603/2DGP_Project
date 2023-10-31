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


def reset_world():
    global running
    global world
    global back_ground

    running = True
    world = []

    back_ground = Burning_city()
    world.append(back_ground)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()

# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.02)

# finalization code
close_canvas()


# lec13 게임 프레임웍 적용준비
# from pico2d import open_canvas, close_canvas
# import game_framework
# # import logo_mode as start_mode
# # import title_mode as start_mode
# import play_mode as start_mode
#
# open_canvas()
# game_framework.run(start_mode)
# close_canvas()

