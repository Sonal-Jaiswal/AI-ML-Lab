import heapq
import pygame
import time
import random


CELL_SIZE = 40

# Define Colors
GRID_COLOR = (240, 240, 240)
WALL_COLOR = (90, 90, 90)
START_COLOR = (34, 177, 76)
TREASURE_COLOR = (255, 223, 0)
EXPLORED_COLOR = (173, 216, 230)
PATH_COLOR = (255, 69, 0)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance heuristic."""
    return abs(x1 - x2) + abs(y1 - y2)

def best_first_search(grid, start, treasure, screen):
    """Best-First Search algorithm with smooth animation."""
    rows, cols = len(grid), len(grid[0])
    start_x, start_y = start
    treasure_x, treasure_y = treasure

    pq = []
    heapq.heappush(pq, (manhattan_distance(start_x, start_y, treasure_x, treasure_y), start_x, start_y))
    
    visited = set()
    visited.add((start_x, start_y))
    
    parent = {}  # To store the path

    while pq:
        h_value, x, y = heapq.heappop(pq)  # Get cell with lowest heuristic value
        
        # Visualization: Mark as explored
        if (x, y) != start and (x, y) != treasure:
            draw_grid(grid, screen, explored=(x, y), start=start, treasure=treasure)
            pygame.time.wait(200)  # Smooth animation delay

        # Check if we reached the treasure
        if (x, y) == treasure:
            path = reconstruct_path(parent, start, treasure)
            draw_grid(grid, screen, path=path, start=start, treasure=treasure)
            print(f"🎉 Treasure found at ({x}, {y})!")
            return path

        # Explore neighbors
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and grid[nx][ny] == 0:
                heapq.heappush(pq, (manhattan_distance(nx, ny, treasure_x, treasure_y), nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)  # Track the path

    print("❌ Treasure not found.")
    return None

def reconstruct_path(parent, start, goal):
    """Reconstruct path from start to goal using parent dictionary."""
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

def draw_grid(grid, screen, explored=None, path=None, start=None, treasure=None):
    """Draw the grid using pygame."""
    screen.fill(GRID_COLOR)
    
    rows, cols = len(grid), len(grid[0])
    
    for i in range(rows):
        for j in range(cols):
            color = GRID_COLOR
            if grid[i][j] == 1:
                color = WALL_COLOR
            elif start and (i, j) == start:
                color = START_COLOR
            elif treasure and (i, j) == treasure:
                color = TREASURE_COLOR
            elif explored and (i, j) == explored:
                color = EXPLORED_COLOR
            elif path and (i, j) in path:
                color = PATH_COLOR
            
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    pygame.display.update()

def get_random_empty_cell(grid):
    """Find a random empty cell (0) for placing the treasure."""
    empty_cells = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    return random.choice(empty_cells)

# Sample Grid (1 = Wall, 0 = Open Path)
grid = [
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
]

# Define Start Position & Random Treasure Placement
start = (0, 0) 
treasure = get_random_empty_cell(grid)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((len(grid[0]) * CELL_SIZE, len(grid) * CELL_SIZE))
pygame.display.set_caption("🏆 Treasure Hunt [By Sonal Jaiswal]")

# Draw Initial Grid
draw_grid(grid, screen, start=start, treasure=treasure)

# Run Best-First Search
best_first_search(grid, start, treasure, screen)

# Keep Window Open Until User Exits
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
