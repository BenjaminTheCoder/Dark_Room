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

character = pr.load_texture("Assets/Dark_room_ball.png")
potf = pr.load_texture("Assets/pot.png")
flashlight = pr.load_texture("Assets/flashlight2.png")
# end = pr.load_texture("Assets/Dark_Room_end.png")



def win_screen(gv: GameVariables) -> None:
    if gv.win == True:
        pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
        pr.draw_text(f'You win!', 275, 270, 60, pr.WHITE)
        # pr.draw_text('Press "Space" to play again', 190, 340, 30, pr.WHITE)
    
def lose_screen(gv: GameVariables) -> None:
    if gv.lose == True:
        pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
        pr.draw_text(f'You lose!', 275, 270, 60, pr.WHITE)
        # pr.draw_text('Press "Space" to play again', 190, 340, 30, pr.WHITE)

def canYouGoThereX(nextX: float, walls: list[pr.Rectangle]) -> bool:
    canGo = True
    for wall in walls:
        if (
            nextX >= wall.x
            and nextX < wall.x + wall.width
        ):
            canGo = False
    return canGo

def canYouGoThereY(nextY: float, walls: list[pr.Rectangle]) -> bool:
    for wall in walls:
        if (
            nextY >= wall.y
            and nextY < wall.height + wall.y
        ):
            canGo = True
        else:    
            canGo = False
    return canGo


def canYouGoThere(nextX: float, nextY: float, walls: list[pr.Rectangle]) -> bool:
    return canYouGoThereX(nextX, walls) and canYouGoThereY(nextY, walls)

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
    #         gv.player.vx *= -1
    #     if gv.player.x > (wall.x - gv.player.r) and gv.player.x < (wall.x + gv.player.r) and gv.player.y > wall.y and gv.player.y < wall.y + wall.height:
    #         gv.player.vx *= -1.

    #     if gv.player.y < (wall.y + wall.height + gv.player.r) and gv.player.y > (wall.y + gv.player.r) and gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
    #         gv.player.vy *= -1
    #     if gv.player.y > (wall.y - gv.player.r) and gv.player.y < (wall.y + gv.player.r) and gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
    #         gv.player.vy *= -1


    if canYouGoThereX(gv.player.x + gv.player.vx, gv.walls):
        print("I can go there!")
        
    else:
        print("Oh no! I cannot go there!")
        # gv.player.vx *= -1
        # gv.player.vy *= -1
    

    for pot in gv.pots:
        if gv.player.x <= (round(pot.x) + round(pot.width) + gv.player.r) and gv.player.x > (round(pot.x) + gv.player.r) and gv.player.y > round(pot.y) and gv.player.y < round(pot.y) + round(pot.height):
            gv.lose = True
        if gv.player.x >= (round(pot.x) - gv.player.r) and gv.player.x < (round(pot.x) + gv.player.r) and gv.player.y > round(pot.y) and gv.player.y < round(pot.y) + round(pot.height):
            gv.lose = True
        if gv.player.y <= (round(pot.y) + round(pot.height) + gv.player.r) and gv.player.y > (round(pot.y) + gv.player.r) and gv.player.x > round(pot.x) and gv.player.x < round(pot.x) + round(pot.width):
            gv.lose = True
        if gv.player.y >= (round(pot.y) - gv.player.r) and gv.player.y < (round(pot.y) + gv.player.r) and gv.player.x > round(pot.x) and gv.player.x < round(pot.x) + round(pot.width):
            gv.lose = True

    if gv.player.x >= gv.end_pos.x and gv.player.y >= gv.end_pos.y:
        gv.win = True


    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    
    for wall in gv.walls:
        pr.draw_rectangle(round(wall.x), round(wall.y), round(wall.width), round(wall.height), pr.BLACK)
    pr.draw_texture(flashlight, round(gv.player.x - gv.player.r)+16-800, round(gv.player.y - gv.player.r)+16-600, pr.WHITE)
    pr.draw_texture(character, round(gv.player.x - gv.player.r), round(gv.player.y - gv.player.r), pr.WHITE)
    pr.draw_circle(int(gv.end_pos.x), int(gv.end_pos.y), gv.end_pos.r, pr.GREEN)
    for pot in gv.pots:
        pr.draw_texture( potf, round(pot.x), round(pot.y), pr.BLUE)
    win_screen(gv)
    lose_screen(gv)
    pr.end_drawing()
pprint.pprint(gv.mazegen.__dict__)
pr.close_window()