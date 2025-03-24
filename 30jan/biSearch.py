import pygame
import random
import collections

pygame.init()
SIZE = 21  
WIDTH, HEIGHT = 600, 600
BOX = WIDTH // SIZE
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bidirectional Maze Solver © Sonal Jaiswal")

def generate_maze():
    grid = [[1] * SIZE for _ in range(SIZE)]
    stack = [(1, 1)]
    grid[1][1] = 0

    while stack:
        r, c = stack[-1]
        neighbors = [(r + dr * 2, c + dc * 2) for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                     if 1 <= r + dr * 2 < SIZE - 1 and 1 <= c + dc * 2 < SIZE - 1 and grid[r + dr * 2][c + dc * 2]]
        
        if neighbors:
            nr, nc = random.choice(neighbors)
            grid[(r + nr) // 2][(c + nc) // 2] = grid[nr][nc] = 0
            stack.append((nr, nc))
        else:
            stack.pop()
    
    return grid


def neighbors(r, c):
    return [(nr, nc) for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if (nr := r + dr, nc := c + dc) and 0 <= nr < SIZE and 0 <= nc < SIZE and grid[nr][nc] == 0]

# Bidirectional BFS implementation
def bidirectional_bfs(start, end):
    queue_s, queue_e = collections.deque([start]), collections.deque([end])
    parent_s, parent_e = {start: None}, {end: None}
    visited_s, visited_e = set([start]), set([end])
    
    while queue_s and queue_e:
        for queue, parent, visited, other_visited in [(queue_s, parent_s, visited_s, visited_e), 
                                                      (queue_e, parent_e, visited_e, visited_s)]:
            if queue:
                node = queue.popleft()
                if node in other_visited:
                    return reconstruct_path(node, parent_s, parent_e), visited_s, visited_e

                for nxt in neighbors(*node):
                    if nxt not in visited:
                        visited.add(nxt)
                        parent[nxt] = node
                        queue.append(nxt)
                
                draw(visited_s, visited_e, node)  
        
    return [], visited_s, visited_e

def reconstruct_path(mid, parent_s, parent_e):
    path = []
    while mid:
        path.append(mid)
        mid = parent_s[mid] if mid in parent_s else parent_e[mid]
    return path[::-1]

def draw(visited_s, visited_e, moving_point=None, path=[]):
    screen.fill(WHITE)
    

    for r in range(SIZE):
        for c in range(SIZE):
            color = WHITE if grid[r][c] == 0 else BLACK
            pygame.draw.rect(screen, color, (c * BOX, r * BOX, BOX, BOX))

    for r, c in visited_s: pygame.draw.rect(screen, BLUE, (c * BOX, r * BOX, BOX, BOX))
    for r, c in visited_e: pygame.draw.rect(screen, BLUE, (c * BOX, r * BOX, BOX, BOX))
    for r, c in path: pygame.draw.rect(screen, GREEN, (c * BOX, r * BOX, BOX, BOX))

    if moving_point:
        pygame.draw.circle(screen, GREEN, (moving_point[1] * BOX + BOX // 2, moving_point[0] * BOX + BOX // 2), BOX // 3)

    pygame.draw.rect(screen, RED, (start[1] * BOX, start[0] * BOX, BOX, BOX))
    pygame.draw.rect(screen, GREEN, (end[1] * BOX, end[0] * BOX, BOX, BOX))
    
    pygame.display.flip()
    pygame.time.wait(40)  


grid = generate_maze()
start, end = (1, 1), (SIZE - 2, SIZE - 2)
path, visited_s, visited_e = bidirectional_bfs(start, end)

path_found = False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Close only when 'Q' is pressed
                running = False
    
    if path and not path_found:
        path_found = True
    
    draw(visited_s, visited_e, path=path)
pygame.quit()
