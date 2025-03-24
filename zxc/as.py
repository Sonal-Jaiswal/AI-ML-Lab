import pygame
import random
from collections import deque
import heapq

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 25
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
START_POS = (GRID_SIZE, GRID_SIZE)
END_POS = (SCREEN_WIDTH - GRID_SIZE * 2, SCREEN_HEIGHT - GRID_SIZE * 2)

# Colors
BLUE = (0, 0, 255)  # Maze walls
YELLOW = (255, 255, 0)  # Maze path
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Start and End points
GREEN = (0, 255, 0)  # Player

# Initialize screen
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Explorer")

# Directions for grid navigation
DIRECTIONS = [(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)]

def draw_maze(obstacles, start, end, player_pos, path):
    surface.fill(BLACK)

    # Draw maze border
    pygame.draw.rect(surface, BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

    # Draw maze obstacles (walls)
    for obstacle in obstacles:
        pygame.draw.rect(surface, BLUE, (*obstacle, GRID_SIZE, GRID_SIZE))

    # Draw start and end points
    pygame.draw.rect(surface, RED, (*start, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, RED, (*end, GRID_SIZE, GRID_SIZE))

    # Draw player position
    pygame.draw.rect(surface, GREEN, (*player_pos, GRID_SIZE, GRID_SIZE))

    # Highlight path
    for dx, dy in path:
        pygame.draw.rect(surface, YELLOW, (dx, dy, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

def generate_maze(grid_size, start, end):
    """Generates a maze using randomized DFS."""
    width, height = SCREEN_WIDTH // grid_size, SCREEN_HEIGHT // grid_size
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def index_to_coords(i, j):
        return j * grid_size, i * grid_size

    def coords_to_index(x, y):
        return y // grid_size, x // grid_size

    stack = []
    start_index = coords_to_index(*start)
    maze[start_index[1]][start_index[0]] = 0
    stack.append(start_index)

    while stack:
        current = stack[-1]
        x, y = current
        neighbors = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx // grid_size, y + dy // grid_size
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                surrounding_paths = 0
                for dx2, dy2 in DIRECTIONS:
                    nx2, ny2 = nx + dx2 // grid_size, ny + dy2 // grid_size
                    if 0 <= nx2 < width and 0 <= ny2 < height:
                        if maze[ny2][nx2] == 0:
                            surrounding_paths += 1
                if surrounding_paths < 2:
                    neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(next_cell)
            maze[next_cell[1]][next_cell[0]] = 0
        else:
            stack.pop()

    end_index = coords_to_index(*end)
    maze[end_index[1]][end_index[0]] = 0

    obstacles = []
    for i in range(height):
        for j in range(width):
            if maze[i][j] == 1:
                obstacles.append(index_to_coords(j, i))

    return obstacles

def bfs(start, target, obstacles):
    visited = set()
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

        if current not in visited:
            visited.add(current)

            for dx, dy in DIRECTIONS:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < SCREEN_WIDTH and
                        0 <= neighbor[1] < SCREEN_HEIGHT and
                        neighbor not in visited and
                        neighbor not in obstacles):
                    queue.append((neighbor, path + [neighbor]))

    return []

def dfs(start, target, obstacles):
    visited = set()
    stack = [(start, [])]

    while stack:
        current, path = stack.pop()

        if current == target:
            return path

        if current not in visited:
            visited.add(current)

            for dx, dy in DIRECTIONS:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < SCREEN_WIDTH and
                        0 <= neighbor[1] < SCREEN_HEIGHT and
                        neighbor not in visited and
                        neighbor not in obstacles):
                    stack.append((neighbor, path + [neighbor]))

    return []

def astar(start, target, obstacles):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start, []))
    g_score = {start: 0}

    while open_set:
        _, current, path = heapq.heappop(open_set)

        if current == target:
            return path

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor in obstacles or not (0 <= neighbor[0] < SCREEN_WIDTH and 0 <= neighbor[1] < SCREEN_HEIGHT):
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, target)
                heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))

    return []

def display_menu():
    surface.fill(BLACK)
    font = pygame.font.Font(None, 48)
    bfs_text = font.render("Press B for BFS", True, WHITE)
    dfs_text = font.render("Press D for DFS", True, WHITE)
    astar_text = font.render("Press A for A*", True, WHITE)
    surface.blit(bfs_text, (100, 150))
    surface.blit(dfs_text, (100, 250))
    surface.blit(astar_text, (100, 350))
    pygame.display.flip()

# Generate Maze
obstacles = generate_maze(GRID_SIZE, START_POS, END_POS)
player_pos = START_POS
path = []

# Menu for choosing algorithm
algorithm = None
while algorithm is None:
    display_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                algorithm = bfs
            elif event.key == pygame.K_d:
                algorithm = dfs
            elif event.key == pygame.K_a:
                algorithm = astar

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not path:
        path = algorithm(player_pos, END_POS, obstacles)
        if not path:
            print("No path found! Game Over.")
            running = False

    if path:
        player_pos = path.pop(0)

    if player_pos == END_POS:
        print("You reached the goal! Congratulations!")
        running = False

    draw_maze(obstacles, START_POS, END_POS, player_pos, path)
    clock.tick(10)

pygame.quit()
