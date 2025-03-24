import heapq
import pygame
import numpy as np
from collections import deque

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Algorithms Visualization")
FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Graph representation for UCS and BFS
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1), ('E', 3)],
    'D': [('E', 2)],
    'E': []
}

positions = {'A': (100, 300), 'B': (250, 200), 'C': (250, 400), 'D': (400, 300), 'E': (550, 300)}

def draw_graph(path=[]):
    """Draws the graph and highlights the path."""
    screen.fill(WHITE)
    for node, edges in graph.items():
        for neighbor, _ in edges:
            pygame.draw.line(screen, BLACK, positions[node], positions[neighbor], 2)
    for node, pos in positions.items():
        color = GREEN if node in path else BLUE
        pygame.draw.circle(screen, color, pos, 30)
        text = FONT.render(node, True, WHITE)
        screen.blit(text, (pos[0] - 10, pos[1] - 10))
    pygame.display.flip()

def uniform_cost_search(start, goal):
    """Performs Uniform Cost Search (UCS) on a weighted graph."""
    priority_queue = [(0, start, [])]  # (cost, node, path)
    visited = set()
    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        draw_graph(path)
        pygame.time.delay(500)
        if node == goal:
            return cost, path
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor, path))
    return float('inf'), []

def bfs(start, goal):
    """Performs BFS on an unweighted graph."""
    queue = deque([(start, [])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        draw_graph(path)
        pygame.time.delay(500)
        if node == goal:
            return path
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                queue.append((neighbor, path))
    return []

start_node, goal_node = 'A', 'D'
cost, ucs_path = uniform_cost_search(start_node, goal_node)
bfs_path = bfs(start_node, goal_node)
print(f"UCS - Minimum cost: {cost}, Path: {ucs_path}")
print(f"BFS - Path: {bfs_path}")

# Keep window open until closed by user
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
