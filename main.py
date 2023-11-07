# lec13 게임 프레임웍 적용준비

from pico2d import open_canvas, close_canvas
import game_framework
# import logo_mode as start_mode
# import title_mode as start_mode
import play_mode as start_mode

open_canvas(1600, 900)
game_framework.run(start_mode)
close_canvas()