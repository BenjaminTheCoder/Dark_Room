import pymunk as pm
from pymunk import Vec2d
import pyray as pr
from constants import *

pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)


space = pm.Space()
# space.gravity = Vec2d(0, -981)

player = pm.Body()
player.position = Vec2d(WINDOWWIDTH/2, -WINDOWHEIGHT/2)


poly = pm.Circle(player, 20)
poly.mass = 10
space.add(player, poly)

print_options = pm.SpaceDebugDrawOptions()
while not pr.window_should_close():

    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()

    # player
    if pr.is_key_down(pr.KeyboardKey.KEY_W) or pr.is_key_down(pr.KeyboardKey.KEY_UP):
        player.velocity = Vec2d(player.velocity.x, player.velocity.y + SLIP)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) > 0.1:
        player.velocity = Vec2d(player.velocity.x, player.velocity.y - SLIP)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y) < -0.1:
        player.velocity = Vec2d(player.velocity.x, player.velocity.y + SLIP)
    if pr.is_key_down(pr.KeyboardKey.KEY_S) or pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        player.velocity = Vec2d(player.velocity.x, player.velocity.y - SLIP)
    if player.position.y - poly.radius <= -WINDOWHEIGHT:
        player.velocity = Vec2d(player.velocity.x, -player.velocity.y)
    if player.position.y + poly.radius > 0:
        player.velocity = Vec2d(player.velocity.x, -player.velocity.y)
    if pr.is_key_down(pr.KeyboardKey.KEY_A) or pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        player.velocity = Vec2d(player.velocity.x - SLIP, player.velocity.y)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) > 0.1:
        player.velocity = Vec2d(player.velocity.x + SLIP, player.velocity.y)
    if pr.is_key_down(pr.KeyboardKey.KEY_D) or pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        player.velocity = Vec2d(player.velocity.x + SLIP, player.velocity.y)
    if pr.get_gamepad_axis_movement(0, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_X) < -0.1:
        player.velocity = Vec2d(player.velocity.x - SLIP, player.velocity.y)
    if player.position.x - poly.radius < 0:
        player.velocity = Vec2d(-player.velocity.x, player.velocity.y)
    if player.position.x + poly.radius >= WINDOWWIDTH:
        player.velocity = Vec2d(-player.velocity.x, player.velocity.y)



    space.step(1/FPS)
    # space.debug_draw(print_options)

    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    pr.draw_circle(round(player.position.x), round(-player.position.y), 20, pr.BLUE)
    pr.end_drawing()
pr.close_window()
