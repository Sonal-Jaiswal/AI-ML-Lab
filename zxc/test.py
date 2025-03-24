import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
BOX_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

# Generate maze grid with multiple paths and guaranteed solution
def generate_maze(rows, cols):
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = 0  # Start point
    grid[rows - 1][cols - 1] = 0  # End point

    # Create a guaranteed random path from start to end
    current = (0, 0)
    path_cells = [current]
    visited = set(path_cells)

    while current != (rows - 1, cols - 1):
        next_steps = [(current[0] + dr, current[1] + dc) for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)] if 0 <= current[0] + dr < rows and 0 <= current[1] + dc < cols and (current[0] + dr, current[1] + dc) not in visited]
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
                break  # No more cells to backtrack to

    # Add random openings to create multiple paths
    for _ in range(rows * cols // 3):
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        grid[r][c] = 0

    return grid

# Draw the maze
def draw_maze(grid, visited=None, path=None):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            color = BLACK if grid[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE))
            pygame.draw.rect(screen, BLUE, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)

    # Highlight visited cells
    if visited:
        for cell in visited:
            row, col = cell
            pygame.draw.rect(screen, GREEN, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE))

    # Highlight path
    if path:
        for row, col in path:
            pygame.draw.rect(screen, RED, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE))

    # Highlight start and end
    pygame.draw.rect(screen, RED, (0, 0, BOX_SIZE, BOX_SIZE))
    pygame.draw.rect(screen, RED, ((COLS - 1) * BOX_SIZE, (ROWS - 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE))

# BFS algorithm
def bfs(grid, start, end):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}

    while queue:
        current = queue.popleft()

        # Visualize the current cell being visited
        draw_maze(grid, visited)
        pygame.display.flip()
        pygame.time.wait(50)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return reconstruct_path(parent, start, end)

# DFS algorithm
def dfs(grid, start, end):
    stack = [start]
    visited = set()
    visited.add(start)
    parent = {}

    while stack:
        current = stack.pop()

        # Visualize the current cell being visited
        draw_maze(grid, visited)
        pygame.display.flip()
        pygame.time.wait(50)

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return reconstruct_path(parent, start, end)

# Get neighbors of a cell
def get_neighbors(grid, cell):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dr, dc in directions:
        r, c = cell[0] + dr, cell[1] + dc
        if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == 0:
            neighbors.append((r, c))
    return neighbors

# Reconstruct path from parent map
def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            return []  # No path found
    path.append(start)
    path.reverse()
    return path

# Display menu
def display_menu():
    font = pygame.font.Font(None, 50)
    screen.fill(WHITE)

    bfs_text = font.render("1. BFS", True, BLACK)
    dfs_text = font.render("2. DFS", True, BLACK)

    screen.blit(bfs_text, (WIDTH // 2 - bfs_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(dfs_text, (WIDTH // 2 - dfs_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

# Display end menu
def display_end_menu():
    font = pygame.font.Font(None, 50)
    screen.fill(WHITE)

    menu_text = font.render("1. Menu", True, BLACK)
    exit_text = font.render("2. Exit", True, BLACK)

    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

# Main function
def main():
    running = True
    while running:
        display_menu()

        grid = generate_maze(ROWS, COLS)
        start = (0, 0)
        end = (ROWS - 1, COLS - 1)

        selected = False
        while not selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        path = bfs(grid, start, end)
                        selected = True
                    elif event.key == pygame.K_2:
                        path = dfs(grid, start, end)
                        selected = True

        display_end_menu()
        end_menu = False

        while not end_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        end_menu = True
                    elif event.key == pygame.K_2:
                        pygame.quit()
                        return

if __name__ == "__main__":
    main()
