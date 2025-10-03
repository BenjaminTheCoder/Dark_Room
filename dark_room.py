import pyray as pr
# from labyrinth import maze # type: ignore
# from labyrinth.grid import Cell, Direction, Grid # type: ignore
from maze_generator_jotbleach import MazeGenerator
from dataclasses import dataclass, field
import pprint
import random as rand
import math



WINDOWWIDTH = 800
WINDOWHEIGHT = 600
MAZE_WIDTH = 11
MAZE_HEIGHT = 11
CELL_WIDTH =  WINDOWWIDTH / MAZE_WIDTH
CELL_HEIGHT = WINDOWHEIGHT / MAZE_HEIGHT
FPS = 120
SLIP = 0.0015
GAMEPAD = 0


def is_odd(number: int) -> bool:
    return number % 2 == 1


assert is_odd(MAZE_WIDTH), "MAZE_WIDTH must be odd!!"
assert is_odd(MAZE_HEIGHT), "MAZE_HEIGHT must be odd!!"


@dataclass
class Circle:
    x: float
    y: float
    r: int
    vx: float
    vy: float

mazegen = MazeGenerator(width=MAZE_WIDTH, height=MAZE_HEIGHT, seed=None)
mazegen.generate_maze()

player = Circle(65, 17, 16, 0, 0)

# test_wall  = pr.Rectangle(300, 200, 100, 100)
# m = (WINDOWWIDTH//line_lengthx, WINDOWHEIGHT//line_lengthy)
#   
mazegen = MazeGenerator(width=MAZE_WIDTH, height=MAZE_HEIGHT, seed=None)
mazegen.generate_maze()




pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

character = pr.load_texture("Assets/Dark_room_ball.png")
flashlight = pr.load_texture("Assets/flashlight2.png")
end = pr.load_texture("Assets/Dark_room_end.png")





while not pr.window_should_close():


    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()


    # Player
    if pr.is_key_down(pr.KeyboardKey.KEY_W) or pr.is_key_down(pr.KeyboardKey.KEY_UP):
        player.vy -= SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) > 0.1:
        player.vy += SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) < -0.1:
        player.vy -= SLIP
    if pr.is_key_down(pr.KeyboardKey.KEY_S) or pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        player.vy += SLIP
    if player.y + player.r <= WINDOWHEIGHT:
        player.vy *= -1
    if player.y - player.r > 0:
        player.vy *= -1
    if pr.is_key_down(pr.KeyboardKey.KEY_A) or pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        player.vx -= SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) > 0.1:
        player.vx += SLIP
    if pr.is_key_down(pr.KeyboardKey.KEY_D) or pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        player.vx += SLIP
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) < -0.1:
        player.vx -= SLIP
    if player.x - player.r < 0:
        player.vx *= -1
    if player.x + player.r >= WINDOWWIDTH:
        player.vx *= -1

    player.x += player.vx
    player.y += player.vy



    walls = []
    for row in range(0, MAZE_HEIGHT):
        for col in range(0, MAZE_WIDTH):
            if mazegen.maze[row][col] == 1:
                wall = pr.Rectangle(col*CELL_WIDTH, row*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)  
                walls.append(wall)

    for wall in walls:
        if player.x < (wall.x + wall.width + player.r) and player.x > (wall.x + player.r) and player.y > wall.y and player.y < wall.y + wall.height:
            player.vx *= -1
        if player.x > (wall.x - player.r) and player.x < (wall.x + player.r) and player.y > wall.y and player.y < wall.y + wall.height:
            player.vx *= -1
        if player.y < (wall.y + wall.height + player.r) and player.y > (wall.y + player.r) and player.x > wall.x and player.x < wall.x + wall.width:
            player.vy *= -1
        if player.y > (wall.y - player.r) and player.y < (wall.y + player.r) and player.x > wall.x and player.x < wall.x + wall.width:
            player.vy *= -1




    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    
    for wall in walls:
        pr.draw_rectangle(round(wall.x), round(wall.y), round(wall.width), round(wall.height), pr.BLACK)

    # pr.draw_texture(flashlight, round(player.x - player.r)+16-800, round(player.y - player.r)+16-600, pr.WHITE)
    pr.draw_texture(character, round(player.x - player.r), round(player.y - player.r), pr.WHITE)
    pr.draw_circle( mazegen.end_pos[0], WINDOWHEIGHT - mazegen.end_pos[1]*2, 16, pr.GREEN)
    pr.end_drawing()
pprint.pprint(mazegen.__dict__)
pr.close_window()