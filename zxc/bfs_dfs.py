import pygame
import time
from collections import deque

# Constants
CELL_SIZE = 50
GRID_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 0)
WALL_COLOR = (0, 0, 255)
FREE_COLOR = (255, 255, 255)
START_COLOR = (0, 0, 0)
END_COLOR = (255, 0, 0)

# Initialize pygame
pygame.init()

def display_maze_pygame(maze, path, start, end, continuous=False):
    rows, cols = len(maze), len(maze[0])
    screen_width, screen_height = cols * CELL_SIZE, rows * CELL_SIZE

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Traversal")

    clock = pygame.time.Clock()

    def draw_maze():
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if maze[y][x] == 0:
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                elif (y, x) == start:
                    pygame.draw.rect(screen, START_COLOR, rect)
                elif (y, x) == end:
                    pygame.draw.rect(screen, END_COLOR, rect)
                else:
                    pygame.draw.rect(screen, FREE_COLOR, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    draw_maze()
    pygame.display.flip()

    # Animate the path
    for position in path:
        for event in pygame.event.get():  # Event handling
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        y, x = position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PATH_COLOR, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        pygame.display.flip()  # Updates the display
        time.sleep(0.2)  # Delay to create the animation effect

        if continuous:
            clock.tick(10)

    # Wait for a few seconds before exiting
    time.sleep(3 if not continuous else 0)

    pygame.quit()

# Maze representation
maze = [
    [1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1],
]

start = (0, 0)
end_row = int(input("Enter the row for the ending point: "))
end_col = int(input("Enter the column for the ending point: "))
end = (end_row, end_col)

print("Starting point:", start)
print("Ending point:", end)

def is_valid(maze, x, y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 1

def bfs(maze, start, end):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent.get(current)
            return path[::-1]

        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if is_valid(maze, nx, ny) and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

    return None

def dfs_with_animation(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    screen_width, screen_height = cols * CELL_SIZE, rows * CELL_SIZE

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("DFS Maze Traversal")

    clock = pygame.time.Clock()

    def draw_maze():
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if maze[y][x] == 0:
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                elif (y, x) == start:
                    pygame.draw.rect(screen, START_COLOR, rect)
                elif (y, x) == end:
                    pygame.draw.rect(screen, END_COLOR, rect)
                else:
                    pygame.draw.rect(screen, FREE_COLOR, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    draw_maze()
    pygame.display.flip()

    stack = [start]
    visited = set()
    visited.add(start)
    parent = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        current = stack.pop()

        y, x = current
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PATH_COLOR, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        pygame.display.flip()
        time.sleep(0.2)

        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent.get(current)
            pygame.quit()
            return path[::-1]

        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if is_valid(maze, nx, ny) and (nx, ny) not in visited:
                stack.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

    pygame.quit()
    return None

# Get BFS path
bfs_path = bfs(maze, start, end)
if bfs_path:
    print("BFS Path:", bfs_path)
    display_maze_pygame(maze, bfs_path, start, end)
else:
    print("No path found!")

# Get DFS path
dfs_path = dfs_with_animation(maze, start, end)
if dfs_path:
    print("DFS Path:", dfs_path)
else:
    print("No path found!")
