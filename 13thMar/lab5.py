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
BLUE = (0, 0, 255)

# Goal state
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # Converted to a tuple

def heuristic_misplaced_tiles(state):
    """H1: Number of misplaced tiles (excluding empty tile)."""
    return sum(state[i][j] != goal_state[i][j] and state[i][j] != 0 for i in range(3) for j in range(3))

def heuristic_manhattan_distance(state):
    """H2: Sum of Manhattan distances of all tiles from their goal positions."""
    total_distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:  # Ignore empty tile
                x, y = divmod(tile - 1, 3)
                total_distance += abs(x - i) + abs(y - j)
    return total_distance

def get_neighbors(state):
    """Returns possible moves from the current state."""
    neighbors = []
    state_list = [list(row) for row in state]  # Convert tuple to mutable list
    x, y = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
    
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state_list]  # Copy state
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(tuple(map(tuple, new_state)))  # Convert back to tuple
    
    return neighbors

def a_star_solver(start_state, heuristic):
    """A* algorithm for solving the 8-puzzle problem."""
    priority_queue = [(heuristic(start_state), 0, start_state, [])]
    visited = set()
    nodes_explored = 0
    
    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        
        if state in visited:
            continue

        path = path + [state]
        visited.add(state)
        nodes_explored += 1

        draw_puzzle(state)
        pygame.time.delay(300)
        
        if state == goal_state:
            return cost, path, nodes_explored
        
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path))
    
    return float('inf'), [], nodes_explored

def draw_puzzle(state):
    """Draws the 8-puzzle state."""
    screen.fill(WHITE)
    tile_size = WIDTH // 3
    
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                pygame.draw.rect(screen, BLUE, (j * tile_size, i * tile_size, tile_size, tile_size))
                text = FONT.render(str(state[i][j]), True, WHITE)
                screen.blit(text, (j * tile_size + tile_size // 3, i * tile_size + tile_size // 3))
    
    pygame.display.flip()

# Initial state of the 8-puzzle (converted to tuple)
start_state = ((1, 2, 3), (4, 0, 5), (6, 7, 8))

# Solve using A* with both heuristics
cost1, path1, nodes1 = a_star_solver(start_state, heuristic_misplaced_tiles)
cost2, path2, nodes2 = a_star_solver(start_state, heuristic_manhattan_distance)

print(f"Misplaced Tiles Heuristic - Cost: {cost1}, Steps: {len(path1)}, Nodes Explored: {nodes1}")
print(f"Manhattan Distance Heuristic - Cost: {cost2}, Steps: {len(path2)}, Nodes Explored: {nodes2}")

# Keep window open until closed by user
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
