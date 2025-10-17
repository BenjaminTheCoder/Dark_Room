import pyray as pr
# from labyrinth import maze # type: ignore
# from labyrinth.grid import Cell, Direction, Grid # type: ignore
from maze_generator_jotbleach import MazeGenerator #type: ignore
from dataclasses import dataclass, field
import pprint
import random as rand
import math


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
MAZE_WIDTH = 17
MAZE_HEIGHT = 11
CELL_WIDTH =  WINDOWWIDTH / MAZE_WIDTH
CELL_HEIGHT = WINDOWHEIGHT / MAZE_HEIGHT
FPS = 120
SLIP = 0.0015
GAMEPAD = 0

@dataclass
class Circle:
    x: float
    y: float
    r: int
    vx: float
    vy: float


@dataclass
class GameVariables:
    mazegen:MazeGenerator = MazeGenerator(width=MAZE_WIDTH, height=MAZE_HEIGHT, seed=None)
    win: bool = False
    player:Circle = field(default_factory=lambda:Circle(65, 17, 16, 0, 0))
    end_pos:Circle = field(default_factory=lambda:Circle(0, 0, 0, 0, 0))

def __post_init__(self:GameVariables) -> None:
    self.end_pos = Circle(round(CELL_WIDTH*(self.mazegen.end_pos[1] + 0.5)), round(CELL_HEIGHT*(self.mazegen.end_pos[0] + 0.5)), 16, 0, 0)


pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

gv = GameVariables()

character = pr.load_texture("Assets/Dark_room_ball.png")
flashlight = pr.load_texture("Assets/flashlight2.png")
# end = pr.load_texture("Assets/Dark_Room_end.png")



def win_screen(win: bool) -> None:
    if win == True:
    # if gv.replay == False:
        pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
        pr.draw_text(f'You win!', 275, 270, 60, pr.WHITE)
        pr.draw_text('Press "Space" to play again', 190, 340, 30, pr.WHITE)

def is_odd(number: int) -> bool:
    return number % 2 == 1


assert is_odd(MAZE_WIDTH), "MAZE_WIDTH must be odd!!"
assert is_odd(MAZE_HEIGHT), "MAZE_HEIGHT must be odd!!"

gv.mazegen.generate_maze()

while not pr.window_should_close():


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



    walls = []
    for row in range(0, MAZE_HEIGHT):
        for col in range(0, MAZE_WIDTH):
            if gv.mazegen.maze[row][col] == 1:
                wall = pr.Rectangle(col*CELL_WIDTH, row*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)  
                walls.append(wall)

    for wall in walls:
        if gv.player.x < (wall.x + wall.width + gv.player.r) and gv.player.x > (wall.x + gv.player.r) and gv.player.y > wall.y and gv.player.y < wall.y + wall.height:
            gv.player.vx *= -1
        if gv.player.x > (wall.x - gv.player.r) and gv.player.x < (wall.x + gv.player.r) and gv.player.y > wall.y and gv.player.y < wall.y + wall.height:
            gv.player.vx *= -1
        if gv.player.y < (wall.y + wall.height + gv.player.r) and gv.player.y > (wall.y + gv.player.r) and gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
            gv.player.vy *= -1
        if gv.player.y > (wall.y - gv.player.r) and gv.player.y < (wall.y + gv.player.r) and gv.player.x > wall.x and gv.player.x < wall.x + wall.width:
            gv.player.vy *= -1

    if gv.player.x >= gv.end_pos.x and gv.player.y >= gv.end_pos.y:
        win = True


    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    
    for wall in walls:
        pr.draw_rectangle(round(wall.x), round(wall.y), round(wall.width), round(wall.height), pr.BLACK)
    pr.draw_texture(flashlight, round(gv.player.x - gv.player.r)+16-800, round(gv.player.y - gv.player.r)+16-600, pr.WHITE)
    pr.draw_texture(character, round(gv.player.x - gv.player.r), round(gv.player.y - gv.player.r), pr.WHITE)
    pr.draw_circle(int(gv.end_pos.x), int(gv.end_pos.y), gv.end_pos.r, pr.GREEN)
    win_screen(win)
    pr.end_drawing()
pprint.pprint(gv.mazegen.__dict__)
pr.close_window()