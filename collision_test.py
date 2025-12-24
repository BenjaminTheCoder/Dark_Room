import pyray as pr
from maze_generator_jotbleach import MazeGenerator #type: ignore
from dataclasses import dataclass, field
import pprint
import random
import math
from constants import *
from class_definitions import GameVariables




pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

gv = GameVariables()


# TODO overwrite gv.walls with a custom single wall
wall = pr.Rectangle(7*CELL_WIDTH, 5*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)  
gv.walls = [wall]

gv.player.r = 5



def canYouGoThere(nextX: float, nextY: float, walls: list[pr.Rectangle]) -> bool:
    canGo = True
    for wall in walls:
        if (
            nextX >= wall.x
            and nextX < wall.x + wall.width
            and nextY >= wall.y
            and nextY < wall.y + wall.height
        ):
            canGo = False
    return canGo




def is_odd(number: int) -> bool:
    return number % 2 == 1


assert is_odd(MAZE_WIDTH), "MAZE_WIDTH must be odd!!"
assert is_odd(MAZE_HEIGHT), "MAZE_HEIGHT must be odd!!"



while not pr.window_should_close():

    if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
                replay = True
                if replay == True:
                    gv = GameVariables()


    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()

    # gv.player
    if pr.is_key_down(pr.KeyboardKey.KEY_W) or pr.is_key_down(pr.KeyboardKey.KEY_UP):
        gv.player.vy -= SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) > 0.1:
        gv.player.vy += SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) < -0.1:
        gv.player.vy -= SLIP
    if pr.is_key_down(pr.KeyboardKey.KEY_S) or pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        gv.player.vy += SLIP
    if gv.player.y + gv.player.r <= WINDOWHEIGHT:
        gv.player.vy *= -1
    if gv.player.y - gv.player.r > 0:
        gv.player.vy *= -1
    if pr.is_key_down(pr.KeyboardKey.KEY_A) or pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        gv.player.vx -= SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) > 0.1:
        gv.player.vx += SLIP
    if pr.is_key_down(pr.KeyboardKey.KEY_D) or pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        gv.player.vx += SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) < -0.1:
        gv.player.vx -= SLIP
    if gv.player.x - gv.player.r < 0:
        gv.player.vx *= -1
    if gv.player.x + gv.player.r >= WINDOWWIDTH:
        gv.player.vx *= -1

    gv.player.x += gv.player.vx
    gv.player.y += gv.player.vy


    # for wall in gv.walls:
    #     if gv.player.x < (wall.x + wall.width + gv.player.r) and gv.player.x > (wall.x + gv.player.r) and gv.player.y > wall.y and gv.player.y < wall.y + wall.height:
    #         # gv.player.vx *= -1
    #         gv.player.collision_horizontal = True
    #     elif gv.player.x > (wall.x - gv.player.r) and gv.player.x < (wall.x + gv.player.r) and gv.player.y > wall.y and gv.player.y < wall.y + wall.height:
    #         # gv.player.vx *= -1
    #         gv.player.collision_horizontal = True

    #     elif gv.player.y < (wall.y + wall.height + gv.player.r) and gv.player.y > (wall.y + gv.player.r) and gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
    #         # gv.player.vy *= -1
    #         gv.player.collision_vertical = True
    #     elif gv.player.y > (wall.y - gv.player.r) and gv.player.y < (wall.y + gv.player.r) and gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
    #         # gv.player.vy *= -1
    #         gv.player.collision_vertical = True
    #     else:
    #         gv.player.collision_vertical = False
    #         gv.player.collision_horizontal = False

    
    

    for wall in gv.walls:

        if gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
            # gv.player.vx *= -1
            gv.player.collision_horizontal = True

        elif gv.player.y > wall.y and gv.player.y < wall.y + wall.height:
            # gv.player.vy *= -1
            gv.player.collision_vertical = True
        else:
            gv.player.collision_vertical = False
            gv.player.collision_horizontal = False

    color = pr.BLUE

    # if canYouGoThere(gv.player.x + gv.player.vx, gv.player.y + gv.player.vy, gv.walls):
    #     gv.player.collision_horizontal = False 
    #     gv.player.collision_vertical = False
    # else:
    #     gv.player.collision_horizontal = True
    #     gv.player.collision_vertical = True
    #     # gv.player.vx *= -1
    #     # gv.player.vy *= -1
    if gv.player.collision_vertical:
        color = pr.RED
    elif gv.player.collision_horizontal:
        color = pr.GREEN
    else:
        color = pr.BLUE    

    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    
    for wall in gv.walls:
        pr.draw_rectangle(round(wall.x), round(wall.y), round(wall.width), round(wall.height), pr.BLACK)

    pr.draw_circle(round(gv.player.x - gv.player.r), round(gv.player.y - gv.player.r), gv.player.r,color)
    pr.end_drawing()
pprint.pprint(gv.mazegen.__dict__)
pr.close_window()