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

global screen, play_button, time, settings_button, quit_button, resume_button, back_button, frame_move, quit_button_title, maze, space, player_body, player_shape, squares, end_trigger, print_options, difficulty_selection, difficulty_selection_cint, difficulty_edit_mode, diffuculty_options_list

def make_box(pos: Vec2d, space: pm.Space, cell_width: float, cell_height: float) -> pm.Body:
    poly_body = pm.Body(body_type=pm.Body.STATIC)
    poly_body.position = pos
    polybox = pm.Poly.create_box(poly_body, (round(cell_width), round(cell_height)))
    polybox.elasticity = ELASTICITY
    polybox.collision_type = 1
    space.add(poly_body, polybox)
    return poly_body

def make_maze(maze_width: int, maze_height: int) -> MazeGenerator: 
    maze = MazeGenerator(maze_width, maze_height, seed=None)
    maze.generate_maze()
    return maze

def build_maze(maze: MazeGenerator, space: pm.Space, cell_width: float, cell_height: float) -> list[pm.Body]:
    walls: list[pm.Body] = []
    for row in range(0, maze_height):
        for col in range(0, maze_width):
            if maze.maze[row][col] == 1:
                wall = make_box(Vec2d(col*cell_width + cell_width // 2, -row*cell_height - cell_height // 2), space, cell_width, cell_height)  
                walls.append(wall)
    return walls

pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")
pr.init_audio_device()

music = pr.load_music_stream('Assets/dark_room_music.mp3')
pr.set_music_volume(music, 0.5)
pr.play_music_stream(music)
dead = pr.load_music_stream('Assets/dark_room_impact.mp3')
pr.set_music_volume(dead, 1.0)
impact_length = pr.get_music_time_length(dead)

# Collision callback
def on_begin(arbiter, space: pm.Space, data) -> None: # type: ignore
    global time, dead
    print("DIE")
    # print(arbiter.shapes)
    time -= 5*FPS
    pr.play_music_stream(dead)
    


# def pm_to_pr(point: Vec2d) -> pr.Vector2:
#     return pr.Vector2(point.x, WINDOWHEIGHT - point.y)




pr.set_target_fps(FPS)

pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

difficulty_selection = 0
difficulty_selection_cint = pr.ffi.new("int *", 0)
difficulty_edit_mode = False
difficulty_options = "EASY;MID;HARD"
diffuculty_options_list = difficulty_options.split(";")
if difficulty_selection == 0:
    maze_width = MAZE_WIDTH_EASY
    maze_height = MAZE_HEIGHT_EASY
    cell_width = CELL_WIDTH_EASY
    cell_height = CELL_HEIGHT_EASY
elif difficulty_selection == 1:
    maze_width = MAZE_WIDTH_MID
    maze_height = MAZE_HEIGHT_MID
    cell_width = CELL_WIDTH_MID
    cell_height = CELL_HEIGHT_MID
elif difficulty_selection == 2:
    maze_width = MAZE_WIDTH_HARD
    maze_height = MAZE_HEIGHT_HARD
    cell_width = CELL_WIDTH_HARD
    cell_height = CELL_HEIGHT_HARD
screen = Screen.TITLE
time = SECONDS*FPS
play_button = 0
settings_button = 0
quit_button = 0   
resume_button = 0
quit_button_title = 0
back_button = 0
frame_move = True
maze = make_maze(maze_width, maze_height)
space = pm.Space()
player_body = pm.Body()
player_body.position = start_pos = Vec2d(round(cell_width*(maze.start_pos[1] + 0.5)), -round(cell_height*(maze.start_pos[0] + 0.5)))
player_shape = pm.Circle(player_body, cell_width/4)
player_shape.mass = 10
player_shape.elasticity = ELASTICITY
player_shape.collision_type = 2
space.add(player_body, player_shape)
space.on_collision(1, 2, begin=on_begin)
squares = build_maze(maze, space, maze_width, maze_height)
end_trigger = Vec2d(round(cell_width*(maze.end_pos[1] + 0.5)), -round(cell_height*(maze.end_pos[0] + 0.5)))
print_options = pm.SpaceDebugDrawOptions()

def reset() -> None:
    global screen, play_button, time, maze_width, maze_height, cell_width, cell_height, settings_button, quit_button, resume_button, back_button, frame_move, quit_button_title, maze, space, player_body, player_shape, squares, end_trigger, print_options, difficulty_selection, difficulty_selection_cint, difficulty_edit_mode, diffuculty_options_list
    if difficulty_selection == 0:
        print("EEEEEEEEEEAAAAAAAAAAAAASSSSSSSSSYYYYYYYYY")
        maze_width = MAZE_WIDTH_EASY
        maze_height = MAZE_HEIGHT_EASY
        cell_width = CELL_WIDTH_EASY
        cell_height = CELL_HEIGHT_EASY
    elif difficulty_selection == 1:
        print("MMMMMMMMIIIIIIIIIIIIIIDDDDDDDDDD")
        maze_width = MAZE_WIDTH_MID
        maze_height = MAZE_HEIGHT_MID
        cell_width = CELL_WIDTH_MID
        cell_height = CELL_HEIGHT_MID
    elif difficulty_selection == 2:
        print("HHHHHHHHHHHHAAAAAAARRRRRRRRRDDDDDDD")
        maze_width = MAZE_WIDTH_HARD
        maze_height = MAZE_HEIGHT_HARD
        cell_width = CELL_WIDTH_HARD
        cell_height = CELL_HEIGHT_HARD
    screen = Screen.TITLE
    time = SECONDS*FPS
    play_button = 0
    settings_button = 0
    quit_button = 0
    resume_button = 0
    quit_button_title = 0
    back_button = 0
    maze = make_maze(maze_width, maze_height)
    space = pm.Space()
    player_body = pm.Body()
    player_body.position = Vec2d(round(cell_width*(maze.start_pos[1] + 0.5)), -round(cell_height*(maze.start_pos[0] + 0.5)))
    player_shape = pm.Circle(player_body, (cell_width+cell_height)//2/4)
    player_shape.mass = 10
    player_shape.elasticity = ELASTICITY
    player_shape.collision_type = 2
    space.add(player_body, player_shape)
    space.on_collision(1, 2, begin=on_begin)
    print(difficulty_selection, maze_width, maze_height, cell_width, cell_height)
    squares = build_maze(maze, space, cell_width, cell_height)
    end_trigger = Vec2d(round(cell_width*(maze.end_pos[1] + 0.5)), -round(cell_height*(maze.end_pos[0] + 0.5)))
    print_options = pm.SpaceDebugDrawOptions()
    # difficulty_selection = 0
    # difficulty_selection_cint = pr.ffi.new("int *", 0)
    # difficulty_edit_mode = False
    # difficulty_options = "EASY;MID;HARD"
    # diffuculty_options_list = difficulty_options.split(";")

flashlight = pr.load_texture("Assets/flashlight2.png")
character = pr.load_texture("Assets/Dark_room_ball.png")




def input_handling(player_body: pm.Body, player_poly: pm.Circle,) -> None:
    global screen
    if pr.is_key_down(pr.KeyboardKey.KEY_F):
        pr.toggle_fullscreen()
    if pr.is_key_down(pr.KeyboardKey.KEY_ESCAPE) and screen == Screen.GAME:
        screen = Screen.PAUSE
    if pr.is_key_down(pr.KeyboardKey.KEY_SPACE) and (screen == Screen.WIN or screen == Screen.LOSE):
        reset()
        screen = Screen.GAME
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
    
sound_time = 0
while not pr.window_should_close():
    pr.update_music_stream(music)
    sound_time += 1
    pr.update_music_stream(dead)
    if sound_time >= 32:
        pr.stop_music_stream(dead)
        sound_time = 0
    

    



    # input handling

    input_handling(player_body, player_shape)

    if screen == Screen.GAME:
        space.step(1/FPS)
    # space.debug_draw(print_options)

    if player_body.position.y < end_trigger.y:
        screen = Screen.WIN
        

# button checks
    if play_button == 1:
        reset()
        screen = Screen.GAME
        play_button = 0

    if settings_button == 1:
        screen = Screen.SETTINGS
        settings_button = 0

    if quit_button == 1:
        screen = Screen.TITLE
        reset()
        quit_button = 0
    
    if resume_button == 1:
        screen = Screen.GAME
        resume_button = 0
    
    if quit_button_title == 1:
        pr.close_window()
        quit_button = 0

    if back_button == 1:
        screen = Screen.TITLE
        back_button = 0
    checked = False

    if time <= 0:
        screen = Screen.LOSE

    if checked == True:
        checked = True

    pr.begin_drawing()
    pr.clear_background((144, 213, 255))


    match screen:
        case Screen.GAME:
            time -= 1
            pr.draw_texture(flashlight, round(player_body.position.x - player_shape.radius)+16-800, round(-player_body.position.y - player_shape.radius)+16-600, pr.BLACK)
            # pr.draw_circle(round(player_body.position.x), round(-player_body.position.y), player_shape.radius, pr.BLUE)
            pr.draw_texture_ex(character, Vec2d(round(player_body.position.x - player_shape.radius), round(-player_body.position.y - player_shape.radius)), 0, (player_shape.radius * 2)/32, pr.WHITE)

            for poly_box in squares:
                pr.draw_rectangle(math.ceil(poly_box.position.x - cell_width / 2), math.ceil(-poly_box.position.y - cell_height / 2), math.ceil(cell_width), math.ceil(cell_height), pr.BLACK)
            pr.draw_text(f'{time//FPS}', WINDOWWIDTH//2-30, 80, 60, pr.WHITE)
            last_box = squares[-1]
            pr.draw_rectangle(math.ceil(last_box.position.x - cell_width / 2) - math.ceil(cell_width), math.ceil(-last_box.position.y - cell_height / 2), math.ceil(cell_width), math.ceil(cell_height), pr.DARKGRAY)

        case Screen.TITLE:
            play_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, WINDOWHEIGHT/2-BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT), "PLAY")
            settings_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, (WINDOWHEIGHT/2-BUTTON_HEIGHT/2+BUTTON_HEIGHT*1.5), BUTTON_WIDTH, BUTTON_HEIGHT), "SETTINGS")
            quit_button_title = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, (WINDOWHEIGHT/2-BUTTON_HEIGHT/2+BUTTON_HEIGHT*3), BUTTON_WIDTH, BUTTON_HEIGHT), "QUIT")


        case Screen.SETTINGS:
            back_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, (WINDOWHEIGHT/2-BUTTON_HEIGHT/2+BUTTON_HEIGHT*1.6), BUTTON_WIDTH, BUTTON_HEIGHT), "BACK")
            if pr.gui_dropdown_box(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, WINDOWHEIGHT/2-BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT), difficulty_options, difficulty_selection_cint, difficulty_edit_mode):
                difficulty_edit_mode = not difficulty_edit_mode
                difficulty_selection = int(difficulty_selection_cint[0])
                print(diffuculty_options_list[difficulty_selection])
                print(difficulty_selection)


        case Screen.PAUSE:
            resume_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, WINDOWHEIGHT/2-BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT), "RESUME")
            quit_button = pr.gui_button(pr.Rectangle(WINDOWWIDTH/2-BUTTON_WIDTH/2, (WINDOWHEIGHT/2-BUTTON_HEIGHT/2+BUTTON_HEIGHT*1.5), BUTTON_WIDTH, BUTTON_HEIGHT), "TITLE")


        case Screen.WIN:
            pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
            pr.draw_text(f'You win!', 275, 270, 60, pr.WHITE)
            pr.draw_text(f'Press SPACE to play again.', 130, 270+80, 40, pr.WHITE)
            if time == 60:
                time = SECONDS*FPS

        case Screen.LOSE:
            pr.draw_rectangle(0, 0, WINDOWWIDTH, WINDOWHEIGHT, pr.BLACK)
            pr.draw_text(f'You lose!', 275, 270, 60, pr.WHITE)     
            pr.draw_text(f'Press SPACE to play again.', 130, 270+80, 40, pr.WHITE)
     

        case _:
            print("Chaos has conquered!!!")
    pr.end_drawing()
pr.close_window()
# pprint(maze.__dict__)
