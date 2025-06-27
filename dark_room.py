import pyray as pr
from dataclasses import dataclass, field
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 120

vel = 1


@dataclass
class Circle:
    x: int
    y: int
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
    if pr.is_key_down(pr.KeyboardKey.KEY_W):
        player.y -= vel
    if pr.is_key_down(pr.KeyboardKey.KEY_S):
        player.y += vel
    if player.y + player.r <= WINDOWHEIGHT:
        player.y += vel
    if player.y - player.r > 0:
        player.y -= vel    
    if pr.is_key_down(pr.KeyboardKey.KEY_A):
        player.x -= vel
    if pr.is_key_down(pr.KeyboardKey.KEY_D):
        player.x += vel
    if player.x - player.r < 0:
       player.x += vel
    if player.x + player.r>=WINDOWWIDTH:
       player.x -= vel

    if player.x < (test_wall.x + test_wall.width + player.r) and player.x > (test_wall.x + player.r) and player.y > test_wall.y and player.y < test_wall.y + test_wall.height:
        player.x += vel
    # if player.x < (test_wall.x + test_wall.width + player.r) and player.x > (test_wall.x + player.r) and player.y > test_wall.y and player.y < test_wall.y + test_wall.height:
    #     player.x += vel



    pr.begin_drawing()
    pr.clear_background((175, 219, 245))
    pr.draw_rectangle(int(test_wall.x), int(test_wall.y), int(test_wall.width), int(test_wall.height), pr.BLACK)
    # pr.draw_circle(player.x, player.y, player.r, pr.BLACK)
    pr.draw_texture(character, player.x - player.r, player.y - player.r, pr.WHITE)
    pr.end_drawing()
pr.close_window()