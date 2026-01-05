def render_maze_with_walls(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Top border
    print("┌" + "───┬" * (cols - 1) + "───┐")

    for r in range(rows):
        # Row of cells
        row_line = "│"
        for c in range(cols):
            if grid[r][c] == 1:
                row_line += " █ │"   # wall cell
            else:
                row_line += "   │"   # open cell
        print(row_line)

        # Row separator (or bottom border)
        if r < rows - 1:
            print("├" + "───┼" * (cols - 1) + "───┤")
        else:
            print("└" + "───┴" * (cols - 1) + "───┘")

maze1 = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]

maze2 = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
]

def run_demo():
    print("Maze 1:")
    render_maze_with_walls(maze1)
    print("\nMaze 2:")
    render_maze_with_walls(maze2)

if __name__ == "__main__":
    run_demo()
