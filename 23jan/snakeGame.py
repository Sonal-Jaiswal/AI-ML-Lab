import pygame
import random
import sys
import time
from collections import deque

GRID_SIZE = 25
TILE_SIZE = 20
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
FPS = 10
APPLE_SPAWN_INTERVAL = 5  
RED_APPLE_DELAY = 10  

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game \u00A9 Sonal Jaiswal ")
clock = pygame.time.Clock()

snake = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
direction = RIGHT
length = 1
apple = None
apple_type = None
last_apple_time = time.time()
start_time = time.time()

def spawn_apple():
    global apple, apple_type
    while True:
        apple = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if apple not in snake:
            break

    if time.time() - start_time >= RED_APPLE_DELAY:
        apple_type = random.choice(["brown", "blue", "red"])
    else:
        apple_type = random.choice(["brown", "blue"])

def draw_grid():
    for x in range(0, WINDOW_SIZE, TILE_SIZE):
        for y in range(0, WINDOW_SIZE, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_snake():
    for segment in snake:
        rect = pygame.Rect(segment[0] * TILE_SIZE, segment[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_apple():
    color = {"brown": BROWN, "blue": BLUE, "red": RED}[apple_type]
    rect = pygame.Rect(apple[0] * TILE_SIZE, apple[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, color, rect)

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path

        for direction in [UP, DOWN, LEFT, RIGHT]:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE and next_pos not in visited and next_pos not in snake:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return []

spawn_apple()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    path = bfs(snake[0], apple)

    if path:
        new_head = path[0]
    else:
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    snake.insert(0, new_head)

    if new_head == apple:
        if apple_type == "brown":
            length = max(1, length // 2)
        elif apple_type == "blue":
            length *= 2
        elif apple_type == "red":
            print("Game Over! You ate a red apple.")
            running = False
            break
        spawn_apple()
    else:
        if len(snake) > length:
            snake.pop()

    if time.time() - last_apple_time > APPLE_SPAWN_INTERVAL and apple_type is None:
        spawn_apple()
        last_apple_time = time.time()

    if new_head in snake[1:] or not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
        print("Game Over! The snake hit its body or the edges.")
        running = False
        break

    screen.fill(BLACK)
    draw_grid()
    draw_snake()
    draw_apple()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
