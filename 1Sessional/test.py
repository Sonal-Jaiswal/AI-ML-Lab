import pygame
import sys
import heapq

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 0, 255)
TREASURE_COLOR = (255, 215, 0)
OBSTRUCTION_COLOR = (255, 0, 0)
BG_COLOR = (200, 255, 200)
PATH_COLOR = (173, 216, 230)

# Positions
start_pos = (2, 2)
treasure_pos = (5, 5)
obstruction_pos = {(1, 1)}

# Directions
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Heuristic (Manhattan Distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Greedy BFS Algorithm
def greedy_bfs(start, goal, obstacles):
    visited = set()
    heap = [(heuristic(start, goal), start)]
    came_from = {}
    
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        visited.add(current)
        for dx, dy in DIRS:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and
                neighbor not in visited and neighbor not in obstacles):
                heapq.heappush(heap, (heuristic(neighbor, goal), neighbor))
                if neighbor not in came_from:
                    came_from[neighbor] = current

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []  # No path found
    path.append(start)
    return path[::-1]

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunter - Greedy BFS")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Drawing
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_objects(player_pos, path):
    screen.fill(BG_COLOR)
    draw_grid()

    # Obstructions
    for obs in obstruction_pos:
        pygame.draw.rect(screen, OBSTRUCTION_COLOR,
                         (obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Path
    for cell in path:
        if cell != treasure_pos and cell != start_pos:
            pygame.draw.rect(screen, PATH_COLOR,
                             (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Treasure
    pygame.draw.rect(screen, TREASURE_COLOR,
                     (treasure_pos[0] * CELL_SIZE, treasure_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Player
    pygame.draw.rect(screen, PLAYER_COLOR,
                     (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Winner message
def show_win_message():
    msg = font.render("Winner Winner Mess Ka Dinner 😋", True, BLACK)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.update()
    pygame.time.delay(3000)

# Main
path = greedy_bfs(start_pos, treasure_pos, obstruction_pos)
player_index = 0
running = True
winner_announced = False

while running:
    clock.tick(4)  # Adjust speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player_index < len(path):
        current_pos = path[player_index]
        draw_objects(current_pos, path)
        player_index += 1
    else:
        draw_objects(treasure_pos, path)
        if not winner_announced:
            show_win_message()
            winner_announced = True

    pygame.display.update()

pygame.quit()
sys.exit()
