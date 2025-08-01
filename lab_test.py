from labyrinth import maze # type: ignore

m = maze.Maze()

nodes = list(m._grid.graph.vertices)

print(nodes)