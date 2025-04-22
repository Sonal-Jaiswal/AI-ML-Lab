import pygame
import sys
import random
from collections import deque
import heapq

pygame.init()

# Config
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Init
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Directions
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # UP, RIGHT, DOWN, LEFT


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))


def get_neighbors(pos):
    neighbors = []
    for dx, dy in DIRS:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            neighbors.append((nx, ny))
    return neighbors


# --- Pathfinding Algorithms ---
def bfs(start, goal, grid):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in came_from and neighbor not in grid:
                queue.append(neighbor)
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)


def dfs(start, goal, grid):
    stack = [start]
    came_from = {start: None}
    while stack:
        current = stack.pop()
        if current == goal:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in came_from and neighbor not in grid:
                stack.append(neighbor)
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan


def a_star(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            break
        for neighbor in get_neighbors(current):
            if neighbor in grid:
                continue
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))
    return reconstruct_path(came_from, start, goal)


def best_first(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in came_from and neighbor not in grid:
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))
    return reconstruct_path(came_from, start, goal)


def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []
    path = []
    while goal != start:
        path.append(goal)
        goal = came_from[goal]
    path.reverse()
    return path


# --- Main Game ---
def main(algo_func):
    snake = [(5, 5)]
    apple = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

    while True:
        screen.fill(BLACK)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid_set = set(snake[1:])
        path = algo_func(snake[0], apple, grid_set)

        if path:
            snake.insert(0, path[0])
        else:
            pygame.quit()
            print("No path to apple!")
            sys.exit()

        if snake[0] == apple:
            while apple in snake:
                apple = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        else:
            snake.pop()

        # Draw apple
        pygame.draw.rect(screen, RED, (*[c * CELL_SIZE for c in apple], CELL_SIZE, CELL_SIZE))
        # Draw snake
        for block in snake:
            pygame.draw.rect(screen, GREEN, (*[c * CELL_SIZE for c in block], CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(FPS)


# Choose the algorithm here:
# main(bfs)
# main(dfs)
main(a_star)
# main(best_first)
