import heapq
import pygame
import numpy as np

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* 8-Puzzle Solver")
FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Goal state
goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

def heuristic_misplaced_tiles(state):
    """Heuristic H1: Counts the number of misplaced tiles."""
    return np.sum((state != goal_state) & (state != 0))

def heuristic_manhattan_distance(state):
    """Heuristic H2: Computes the sum of Manhattan distances."""
    total_distance = 0
    for i in range(3):
        for j in range(3):
            if state[i, j] != 0:
                x, y = divmod(state[i, j] - 1, 3)
                total_distance += abs(x - i) + abs(y - j)
    return total_distance

def get_neighbors(state):
    """Returns possible moves from the current state."""
    neighbors = []
    x, y = np.where(state == 0)
    x, y = x[0], y[0]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = state.copy()
            new_state[x, y], new_state[nx, ny] = new_state[nx, ny], new_state[x, y]
            neighbors.append(new_state)
    
    return neighbors

def a_star_solver(start_state, heuristic):
    """A* algorithm for solving the 8-puzzle problem."""
    priority_queue = [(heuristic(start_state), 0, start_state, [])]
    visited = set()
    
    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        state_tuple = tuple(map(tuple, state))
        
        if state_tuple in visited:
            continue
        
        path = path + [state]
        visited.add(state_tuple)
        
        draw_puzzle(state)
        pygame.time.delay(500)
        
        if np.array_equal(state, goal_state):
            return cost, path
        
        for neighbor in get_neighbors(state):
            if tuple(map(tuple, neighbor)) not in visited:
                heapq.heappush(priority_queue, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path))
    
    return float('inf'), []

def draw_puzzle(state):
    """Draws the 8-puzzle state."""
    screen.fill(WHITE)
    tile_size = WIDTH // 3
    
    for i in range(3):
        for j in range(3):
            if state[i, j] != 0:
                pygame.draw.rect(screen, BLUE, (j * tile_size, i * tile_size, tile_size, tile_size))
                text = FONT.render(str(state[i, j]), True, WHITE)
                screen.blit(text, (j * tile_size + tile_size // 3, i * tile_size + tile_size // 3))
    
    pygame.display.flip()

# Initial state of the 8-puzzle
start_state = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

# Solve using A* with both heuristics
cost1, path1 = a_star_solver(start_state, heuristic_misplaced_tiles)
cost2, path2 = a_star_solver(start_state, heuristic_manhattan_distance)

print(f"Misplaced Tiles Heuristic - Cost: {cost1}, Steps: {len(path1)}")
print(f"Manhattan Distance Heuristic - Cost: {cost2}, Steps: {len(path2)}")

# Keep window open until closed by user
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
