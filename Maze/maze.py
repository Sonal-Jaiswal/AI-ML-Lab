import pygame
import random
from collections import deque

pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
BOX_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver © Sonal Jaiswal")
clock = pygame.time.Clock()


def generate_maze(rows, cols):
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = 0
    grid[rows - 1][cols - 1] = 0

    current = (0, 0)
    path_cells = [current]
    visited = set(path_cells)

    while current != (rows - 1, cols - 1):
        next_steps = [(current[0] + dr, current[1] + dc) for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)] if
                      0 <= current[0] + dr < rows and 0 <= current[1] + dc < cols and (
                      current[0] + dr, current[1] + dc) not in visited]
        if next_steps:
            next_step = random.choice(next_steps)
            grid[next_step[0]][next_step[1]] = 0
            path_cells.append(next_step)
            visited.add(next_step)
            current = next_step
        else:
            if path_cells:
                current = path_cells.pop()
            else:
                break

    for _ in range(rows * cols // 3):
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        grid[r][c] = 0

    return grid


def draw_cell(row, col, color):
    pygame.draw.rect(screen, color, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE))
    pygame.draw.rect(screen, BLUE, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)


def draw_maze(grid, visited=None, path=None):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            color = BLACK if grid[row][col] == 1 else WHITE
            draw_cell(row, col, color)

    if visited:
        for cell in visited:
            draw_cell(*cell, GREEN)

    if path:
        for cell in path:
            draw_cell(*cell, YELLOW)

    draw_cell(0, 0, RED)
    draw_cell(ROWS - 1, COLS - 1, RED)


def bfs(grid, start, end):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}
    distance = {start: 0}

    while queue:
        current = queue.popleft()
        draw_cell(*current, GREEN)
        pygame.display.flip()
        pygame.time.delay(30)

        if current == end:
            return reconstruct_path(parent, start, end)

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)

    return []


def dfs(grid, start, end):
    stack = [start]
    visited = set()
    visited.add(start)
    parent = {}
    distance = {start: 0}

    while stack:
        current = stack.pop()
        draw_cell(*current, GREEN)
        pygame.display.flip()
        pygame.time.delay(30)

        if current == end:
            return reconstruct_path(parent, start, end)

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                distance[neighbor] = distance[current] + 1
                stack.append(neighbor)

    return []


def get_neighbors(grid, cell):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = [(cell[0] + dr, cell[1] + dc) for dr, dc in directions if
                 0 <= cell[0] + dr < ROWS and 0 <= cell[1] + dc < COLS and grid[cell[0] + dr][cell[1] + dc] == 0]
    return neighbors


def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path


def main():
    grid = generate_maze(ROWS, COLS)
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)
    path = []

    running = True
    while running:
        screen.fill(WHITE)
        draw_maze(grid, path=path)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    path = bfs(grid, start, end)
                elif event.key == pygame.K_2:
                    path = dfs(grid, start, end)

    pygame.quit()


if __name__ == "__main__":
    main()