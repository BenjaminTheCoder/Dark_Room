import pyray as pr
from labyrinth import maze # type: ignore
from labyrinth.grid import Cell, Direction, Grid # type: ignore
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

walls = []
nodes_: list[Circle] = []


Line = tuple[pr.Vector2, pr.Vector2]

def maze_to_lines(maze: maze.Maze, line_length: int) -> list[Line]:
    lines: list[Line] = []
    # print('maze', maze._grid, maze.walls)
    for row in range(maze.height):
        for column in range(maze.width):
            cell = maze[row, column]
            print('row', row, 'col', column, 'cell', cell, 'open_walls', cell.open_walls)
            p1 = (column * line_length, row * line_length)
            p2 = (column * line_length * 0.9, (row + 1) * line_length * 0.9)
            point1 = pr.Vector2(p1[0], p1[1])
            point2 = pr.Vector2(p2[0], p2[1])
            print('points', (p1, p2))
            lines.append((point1, point2))
            break
        #     if not Direction.E in cell.open_walls:
        #         point1 = pr.Vector2(column * line_length, row * line_length)
        #         point2 = pr.Vector2(column * line_length, (row + 1) * line_length)
        #         lines.append((point1, point2))
        # for column in range(maze.width):
        #     if not Direction.S in maze[row, column].open_walls:
        #         point1 = pr.Vector2(column * line_length, row * line_length)
        #         point2 = pr.Vector2((column + 1) * line_length, row * line_length)
        #         lines.append((point1, point2))
    return lines

pr.init_window(WINDOWWIDTH, WINDOWHEIGHT, "Dark Room")

pr.set_target_fps(FPS)

character = pr.load_texture("Assets/Dark_room_ball.png")

m = maze.Maze(12, 10)
LINE_LENGTH = 50 

m_lines = maze_to_lines(m, LINE_LENGTH)

nodes = list(m._grid.graph.vertices)

edges = list(m._grid.graph.edges)
print('edges', edges)

for node in nodes:
        node = Circle((node.column*LINE_LENGTH)+(LINE_LENGTH//2), (node.row*LINE_LENGTH)+(LINE_LENGTH//2), 2, 0, 0)
        nodes_.append(node)

edge_lines = []
for edge in edges:
    cell1, cell2 = edge
    edge_p1 = pr.Vector2((cell1.column*LINE_LENGTH)+(LINE_LENGTH//2), (cell1.row*LINE_LENGTH)+(LINE_LENGTH//2))
    edge_p2 = pr.Vector2((cell2.column*LINE_LENGTH)+(LINE_LENGTH//2), (cell2.row*LINE_LENGTH)+(LINE_LENGTH//2))
    edge_lines.append((edge_p1, edge_p2))


for edge in edges:
        wall = (edge)
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

    

    # for wall in walls:
    #     if player.x < (wall.x + wall.width + player.r) and player.x > (wall.x + player.r) and player.y > wall.y and player.y < wall.y + wall.height:
    #         player.vx *= -1
    #     if player.x > (wall.x - player.r) and player.x < (wall.x + player.r) and player.y > wall.y and player.y < wall.y + wall.height:
    #         player.vx *= -1
    #     if player.y < (wall.y + wall.height + player.r) and player.y > (wall.y + player.r) and player.x > wall.x and player.x < wall.x + wall.width:
    #         player.vy *= -1
    #     if player.y > (wall.y - player.r) and player.y < (wall.y + player.r) and player.x > wall.x and player.x < wall.x + wall.width:
    #         player.vy *= -1

    pr.begin_drawing()
    pr.clear_background((144, 213, 255))
    
    # for wall in walls:
    #     # node1 = wall[0]
    #     # node2 = wall[1]
    #     node1, node2 = wall
    #     vec1 = pr.Vector2(node1.column * 20, node1.row * 20)
    #     vec2 = pr.Vector2(node2.column * 20, node2.row * 20)
    #     pr.draw_line_ex(vec1, vec2, 2, pr.BLUE,)

    # for m_line in m_lines:
    #     point1, point2 = m_line
    #     pr.draw_line_ex(point1, point2, 6, pr.BLUE)

    for edge_line in edge_lines:
        point1, point2 = edge_line
        pr.draw_line_ex(point1, point2, 6, pr.GREEN)


    for node in nodes_:
        pr.draw_circle(node.x, node.y, node.r, pr.BLACK)

    pr.draw_texture(character, int(player.x - player.r), int(player.y - player.r), pr.WHITE)
    pr.end_drawing()
pr.close_window()