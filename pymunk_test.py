import pymunk as pm
from pymunk import Vec2d
import pyray as pr
from constants import *
from maze_generator_jotbleach import MazeGenerator #type: ignore
from class_definitions import *
from pprint import pprint
import math
from enum import Enum, auto

class Screen(Enum):
    TITLE = auto()
    GAME = auto()
    SETTINGS = auto()
    PAUSE = auto()
    WIN = auto()
    LOSE = auto()



def make_box(pos: Vec2d, space: pm.Space) -> pm.Body:
    poly_body = pm.Body(body_type=pm.Body.STATIC)
    poly_body.position = pos
    polybox = pm.Poly.create_box(poly_body, (round(CELL_WIDTH), round(CELL_HEIGHT)))
    polybox.elasticity = ELASTICITY
    space.add(poly_body, polybox)
    return poly_body

def make_maze() -> MazeGenerator:
    maze = MazeGenerator(width=MAZE_WIDTH, height=MAZE_HEIGHT, seed=None)
    maze.generate_maze()
    return maze

def build_maze(maze: MazeGenerator, space: pm.Space) -> list[pm.Body]:
    walls: list[pm.Body] = []
    for row in range(0, MAZE_HEIGHT):
        for col in range(0, MAZE_WIDTH):
            if maze.maze[row][col] == 1:
                wall = make_box(Vec2d(col*CELL_WIDTH + CELL_WIDTH // 2, -row*CELL_HEIGHT - CELL_HEIGHT // 2), space)  
                walls.append(wall)
    return walls


# def pm_to_pr(point: Vec2d) -> pr.Vector2:
#     return pr.Vector2(point.x, WINDOWHEIGHT - point.y)


pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

screen = Screen.TITLE
play_button = 0
settings_button = 0
maze = make_maze()

space = pm.Space()
# space.gravity = Vec2d(0, -981)
# space.gravity = Vec2d(981, 0)

player_body = pm.Body()
player_body.position = start_pos = Vec2d(round(CELL_WIDTH*(maze.start_pos[1] + 0.5)), -round(CELL_HEIGHT*(maze.start_pos[0] + 0.5)))

player_shape = pm.Circle(player_body, CELL_WIDTH/4)
player_shape.mass = 10
player_shape.elasticity = ELASTICITY
space.add(player_body, player_shape)

squares = build_maze(maze, space)

end_trigger = Vec2d(round(CELL_WIDTH*(maze.end_pos[1] + 0.5)), -round(CELL_HEIGHT*(maze.end_pos[0] + 0.5)))

print_options = pm.SpaceDebugDrawOptions()

def input_handling(player_body: pm.Body, player_poly: pm.Circle,) -> None:
    global screen
    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()
    if pr.is_key_down(pr.KeyboardKey.KEY_ESCAPE) and screen == Screen.GAME:
        screen = Screen.PAUSE
    if pr.is_key_down(pr.KeyboardKey.KEY_W) or pr.is_key_down(pr.KeyboardKey.KEY_UP):
        player_body.velocity = Vec2d(player_body.velocity.x, player_body.velocity.y + SLIP)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) > 0.1:
        player_body.velocity = Vec2d(player_body.velocity.x, player_body.velocity.y - SLIP)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) < -0.1:
        player_body.velocity = Vec2d(player_body.velocity.x, player_body.velocity.y + SLIP)
    if pr.is_key_down(pr.KeyboardKey.KEY_S) or pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        player_body.velocity = Vec2d(player_body.velocity.x, player_body.velocity.y - SLIP)
    if player_body.position.y - player_poly.radius <= -WINDOWHEIGHT:
        player_body.velocity = Vec2d(player_body.velocity.x, -player_body.velocity.y)
    if player_body.position.y + player_poly.radius > 0:
        player_body.velocity = Vec2d(player_body.velocity.x, -player_body.velocity.y)
    if pr.is_key_down(pr.KeyboardKey.KEY_A) or pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        player_body.velocity = Vec2d(player_body.velocity.x - SLIP, player_body.velocity.y)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) > 0.1:
        player_body.velocity = Vec2d(player_body.velocity.x + SLIP, player_body.velocity.y)
    if pr.is_key_down(pr.KeyboardKey.KEY_D) or pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        player_body.velocity = Vec2d(player_body.velocity.x + SLIP, player_body.velocity.y)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) < -0.1:
        player_body.velocity = Vec2d(player_body.velocity.x - SLIP, player_body.velocity.y)
    if player_body.position.x - player_poly.radius < 0:
        player_body.velocity = Vec2d(-player_body.velocity.x, player_body.velocity.y)
    if player_body.position.x + player_poly.radius >= WINDOWWIDTH:
        player_body.velocity = Vec2d(-player_body.velocity.x, player_body.velocity.y)

while not pr.window_should_close():

    # input handling

    input_handling(player_body, player_shape)

    space.step(1/FPS)
    # space.debug_draw(print_options)

    if player_body.position.y < end_trigger.y:
        screen = Screen.WIN

# button checks
    if play_button == 1:
        screen = Screen.GAME
        play_button = 0

    if settings_button == 1:
        screen = Screen.SETTINGS
        settings_button = 0

    pr.begin_drawing()
    pr.clear_background((144, 213, 255))

    match screen:
        case Screen.GAME:
            pr.draw_circle(round(player_body.position.x), round(-player_body.position.y), player_shape.radius, pr.BLUE)
            # pr.draw_rectangle(math.ceil(end_trigger.x - CELL_WIDTH / 2), math.ceil(-end_trigger.y - CELL_HEIGHT / 2), math.ceil(CELL_WIDTH), math.ceil(CELL_HEIGHT), pr.GREEN)
            for poly_box in squares:
                pr.draw_rectangle(math.ceil(poly_box.position.x - CELL_WIDTH / 2), math.ceil(-poly_box.position.y - CELL_HEIGHT / 2), math.ceil(CELL_WIDTH), math.ceil(CELL_HEIGHT), pr.BLACK)
            

        case Screen.TITLE:
            play_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, WINDOWHEIGHT/2-BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT), "PLAY")
            settings_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, (WINDOWHEIGHT/2-BUTTON_HEIGHT/2+BUTTON_HEIGHT*1.5), BUTTON_WIDTH, BUTTON_HEIGHT), "SETTINGS")

        case Screen.SETTINGS:
            print("Settings")

        case Screen.PAUSE:
            print("Pause") 

        case Screen.WIN:
            pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
            pr.draw_text(f'You win!', 275, 270, 60, pr.WHITE)

        case Screen.LOSE:
            pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
            pr.draw_text(f'You lose!', 275, 270, 60, pr.WHITE)          

        case _:
            print("Chaos has conquered!!!")
    pr.end_drawing()
pr.close_window()
pprint(maze.__dict__)
