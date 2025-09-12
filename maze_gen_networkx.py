# type: ignore
from pprint import pprint
from maze_generator_jotbleach import MazeGenerator

# Create a MazeGenerator object with specified dimensions
maze = MazeGenerator(width=60, height=30, seed=42)

# Generate the maze
maze.generate_maze()

# # Retrieve the maze as a grid (2D list)
# maze_grid = maze.set_maze()

# Visualize the generated maze
# pprint(maze.__dict__)
maze.visualize_maze()


# Save the visualization as an image
# maze.visualize_maze(save_path='desktop_maze.png')

# {'end_pos': (4, 3),
#  'height': 5,
#  'maze': [[1, 0, 1, 1, 1],
#           [1, 0, 0, 0, 1],
#           [1, 1, 1, 0, 1],
#           [1, 0, 0, 0, 1],
#           [1, 1, 1, 0, 1]],
#  'seed': 42,
#  'start_pos': (0, 1),
#  'width': 5}