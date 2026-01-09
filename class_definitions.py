from dataclasses import dataclass, field
from maze_generator_jotbleach import MazeGenerator #type: ignore
import pyray as pr
import random
from constants import *
import pymunk as pm


@dataclass
class Circle:
    x: float
    y: float
    r: int
    vx: float
    vy: float
    collision_horizontal: bool
    collision_vertical: bool


@dataclass
class GameVariables:
    mazegen:MazeGenerator = field(default_factory=lambda: MazeGenerator(width=MAZE_WIDTH, height=MAZE_HEIGHT, seed=None))
    win: bool = False
    lose: bool = False
    player:Circle = field(default_factory=lambda:Circle(65, 17, 16, 0, 0, False, False))
    end_pos:Circle = field(default_factory=lambda:Circle(0, 0, 16, 0, 0, False, False))
    replay:bool = False
    walls:list[pr.Rectangle] = field(default_factory=lambda:list())
    pots:list[pr.Rectangle] = field(default_factory=lambda:list())

    def __post_init__(self) -> None: 
        self.mazegen.generate_maze()
        self.end_pos = Circle(round(CELL_WIDTH*(self.mazegen.end_pos[1] + 0.5)), round(CELL_HEIGHT*(self.mazegen.end_pos[0] + 0.5)), 16, 0, 0, False, False)
        for row in range(0, MAZE_HEIGHT):
            for col in range(0, MAZE_WIDTH):
                if self.mazegen.maze[row][col] == 1:
                    wall = pr.Rectangle(col*CELL_WIDTH, row*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)  
                    self.walls.append(wall)


        for i in range(POTS):
            pot = pr.Rectangle(random.randint(1, MAZE_WIDTH)*CELL_WIDTH, random.randint(1, MAZE_HEIGHT)*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)  
            self.pots.append(pot)

        
        # TODO Set player position based on self.mazegen.start_pos

        # Temporarily set the player position above the end_pos to quickly check for the win condition.
        # self.player.x = self.end_pos.x
        # self.player.y = self.end_pos.y - 20 