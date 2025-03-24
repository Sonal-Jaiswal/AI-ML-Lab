import pygame
import heapq
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (160, 32, 240)

def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_path(screen, path, color):
    for row, col in path:
        pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def get_neighbors(row, col):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = [(row + dr, col + dc) for dr, dc in directions]
    return [(r, c) for r, c in neighbors if 0 <= r < ROWS and 0 <= c < COLS]

def bfs(start, goal):
    queue = [(start, [start])]
    visited = set()
    
    while queue:
        (row, col), path = queue.pop(0)
        if (row, col) == goal:
            return path
        
        if (row, col) not in visited:
            visited.add((row, col))
            for neighbor in get_neighbors(row, col):
                queue.append((neighbor, path + [neighbor]))
    return None

def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    
    while stack:
        (row, col), path = stack.pop()
        if (row, col) == goal:
            return path
        
        if (row, col) not in visited:
            visited.add((row, col))
            for neighbor in get_neighbors(row, col):
                stack.append((neighbor, path + [neighbor]))
    return None

def uniform_cost_search(start, goal):
    open_set = [(0, start, [start])]
    visited = set()
    
    while open_set:
        cost, (row, col), path = heapq.heappop(open_set)
        if (row, col) == goal:
            return path
        
        if (row, col) not in visited:
            visited.add((row, col))
            for neighbor in get_neighbors(row, col):
                heapq.heappush(open_set, (cost + 1, neighbor, path + [neighbor]))
    return None

def greedy_best_first_search(start, goal):
    open_set = [(0, start, [start])]
    visited = set()
    
    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    while open_set:
        _, (row, col), path = heapq.heappop(open_set)
        if (row, col) == goal:
            return path
        
        if (row, col) not in visited:
            visited.add((row, col))
            for neighbor in get_neighbors(row, col):
                heapq.heappush(open_set, (heuristic(neighbor), neighbor, path + [neighbor]))
    return None

def a_star(start, goal):
    open_set = [(0, start, [start])]
    visited = set()
    
    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    while open_set:
        _, (row, col), path = heapq.heappop(open_set)
        if (row, col) == goal:
            return path
        
        if (row, col) not in visited:
            visited.add((row, col))
            for neighbor in get_neighbors(row, col):
                heapq.heappush(open_set, (len(path) + heuristic(neighbor), neighbor, path + [neighbor]))
    return None

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualization")
    
    start, goal = (random.randint(0, ROWS-1), random.randint(0, COLS-1)), (random.randint(0, ROWS-1), random.randint(0, COLS-1))
    bfs_path = bfs(start, goal)
    dfs_path = dfs(start, goal)
    ucs_path = uniform_cost_search(start, goal)
    gbfs_path = greedy_best_first_search(start, goal)
    a_star_path = a_star(start, goal)
    
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(screen)
        
        # if bfs_path:
        #     draw_path(screen, bfs_path, GREEN)
        # if dfs_path:
        #     draw_path(screen, dfs_path, ORANGE)
        # if ucs_path:
        #     draw_path(screen, ucs_path, YELLOW)
        if gbfs_path:
            draw_path(screen, gbfs_path, PURPLE)
        # if a_star_path:
        #     draw_path(screen, a_star_path, BLUE)
        
        pygame.draw.rect(screen, RED, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()