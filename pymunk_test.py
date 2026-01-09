import pymunk as pm
from pymunk import Vec2d
import pyray as pr
from constants import *
from maze_generator_jotbleach import MazeGenerator #type: ignore
from class_definitions import *
from pprint import pprint
import math

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

maze = make_maze()

space = pm.Space()
# space.gravity = Vec2d(0, -981)

player_body = pm.Body()
player_body.position = Vec2d(WINDOWWIDTH/2, -WINDOWHEIGHT/2 + 100)

player_shape = pm.Circle(player_body, 1)
player_shape.mass = 10
player_shape.elasticity = ELASTICITY
space.add(player_body, player_shape)

squares = build_maze(maze, space)



print_options = pm.SpaceDebugDrawOptions()

def input_handling(player_body: pm.Body, player_poly: pm.Circle) -> None:
    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()
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

    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    pr.draw_circle(round(player_body.position.x), round(-player_body.position.y), player_shape.radius, pr.BLUE)
    for poly_box in squares:
        pr.draw_rectangle(math.ceil(poly_box.position.x - CELL_WIDTH / 2), math.ceil(-poly_box.position.y - CELL_HEIGHT / 2), math.ceil(CELL_WIDTH), math.ceil(CELL_HEIGHT), pr.BLACK)

    pr.end_drawing()
pr.close_window()
pprint(maze.__dict__)
