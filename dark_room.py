import pyray as pr
from dataclasses import dataclass, field
import random as rand

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
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

player = Circle(64, 64, 16, 0, 0)

# test_wall  = pr.Rectangle(300, 200, 100, 100)

walls: list[pr.Rectangle] = []

pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

character = pr.load_texture("Assets/Dark_room_ball.png")


for i in range(100):
        wall = pr.Rectangle(rand.randint(75, 750), rand.randint(75, 550), rand.randint(30, 50), rand.randint(30, 50))
        walls.append(wall)

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
        pr.draw_rectangle(int(wall.x), int(wall.y), int(wall.width), int(wall.height), pr.BLACK)
    # pr.draw_circle(int(player.x), int(player.y), player.r, pr.BLACK)
    pr.draw_texture(character, int(player.x - player.r), int(player.y - player.r), pr.WHITE)
    pr.end_drawing()
pr.close_window()