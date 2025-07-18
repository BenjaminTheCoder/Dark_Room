import pyray as pr
from dataclasses import dataclass, field
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 120

vel = 1

gampad = 0

@dataclass
class Circle:
    x: float
    y: float
    r: int

player = Circle(64, 64, 16)

test_wall  = pr.Rectangle(300, 200, 100, 100)

pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

character = pr.load_texture("Assets/Dark_room_ball.png")

while not pr.window_should_close():


    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()


    # Player
    if pr.is_key_down(pr.KeyboardKey.KEY_W) or pr.is_key_down(pr.KeyboardKey.KEY_UP):
        player.y -= vel
    if pr.is_key_released(pr.KeyboardKey.KEY_W) or pr.is_key_released(pr.KeyboardKey.KEY_UP):
        player.y -= vel*5
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) < 0.01:
        player.y -= vel
    if pr.is_key_down(pr.KeyboardKey.KEY_S) or pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        player.y += vel
    if pr.is_key_released(pr.KeyboardKey.KEY_S) or pr.is_key_released(pr.KeyboardKey.KEY_DOWN):
        player.y -= vel*5
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) > -0.01:
        player.y += vel
    if player.y + player.r <= WINDOWHEIGHT:
        player.y += vel
    if player.y - player.r > 0:
        player.y -= vel    
    if pr.is_key_down(pr.KeyboardKey.KEY_A) or pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        player.x -= vel
    if pr.is_key_released(pr.KeyboardKey.KEY_A) or pr.is_key_released(pr.KeyboardKey.KEY_LEFT):
        player.x -= vel*5
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) < 0.01:
        player.x -= vel
    if pr.is_key_down(pr.KeyboardKey.KEY_D) or pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        player.x += vel
    if pr.is_key_released(pr.KeyboardKey.KEY_D) or pr.is_key_released(pr.KeyboardKey.KEY_RIGHT):
        player.x += vel*5
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) > -0.01:
        player.x += vel
    if player.x - player.r < 0:
       player.x += vel
    if player.x + player.r>=WINDOWWIDTH:
       player.x -= vel

    

    if player.x < (test_wall.x + test_wall.width + player.r) and player.x > (test_wall.x + player.r) and player.y > test_wall.y and player.y < test_wall.y + test_wall.height:
        player.x += vel
    if player.x > (test_wall.x - player.r) and player.x < (test_wall.x + player.r) and player.y > test_wall.y and player.y < test_wall.y + test_wall.height:
        player.x -= vel
    if player.y < (test_wall.y + test_wall.height + player.r) and player.y > (test_wall.y + player.r) and player.x > test_wall.x and player.x < test_wall.x + test_wall.width:
        player.y += vel
    if player.y > (test_wall.y - player.r) and player.y < (test_wall.y + player.r) and player.x > test_wall.x and player.x < test_wall.x + test_wall.width:
        player.y -= vel



    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    pr.draw_rectangle(int(test_wall.x), int(test_wall.y), int(test_wall.width), int(test_wall.height), pr.BLACK)
    # pr.draw_circle(player.x, player.y, player.r, pr.BLACK)
    pr.draw_texture(character, int(player.x) - player.r, int(player.y) - player.r, pr.WHITE)
    pr.end_drawing()
pr.close_window()