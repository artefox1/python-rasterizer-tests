import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

point0 = [100, 250]
point1 = [600, 500]
dragging = None
r = 50

def bresenham_h(x0, y0, x1, y1, screen, color):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    i = 1
    if dy < 0:
        i = -1
        dy = -dy
    y = y0
    p = 2 * dy - dx
    for x in range(x0, x1):
        screen.set_at((x, y), color)

        if p > 0:
            y += i
            p = p - 2 * dx
        p = p + 2 * dy

def bresenham_v(x0, y0, x1, y1, screen, color):
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    i = 1
    if dx < 0:
        i = -1
        dx = -dx
    x = x0
    p = 2 * dx - dy
    for y in range(y0, y1):
        screen.set_at((x, y), color)

        if p > 0:
            x += i
            p = p - 2 * dy
        p = p + 2 * dx

def bresenham(x0, y0, x1, y1, screen, color):
    if abs(x1 - x0) > abs(y1 - y0):
        bresenham_h(x0, y0, x1, y1, screen, color)
    else:
        bresenham_v(x0, y0, x1, y1, screen, color)

def draw():
    bresenham(point0[0], point0[1], point1[0], point1[1], screen, WHITE)
    pygame.display.flip()

running = True
while running:
    screen.fill(BLACK)
    dt = clock.tick(60) / 1000
    print(clock.get_fps())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if (point0[0] - r <= mx <= point0[0] + r) and (point0[1] - r <= my <= point0[1] + r):
                dragging = "point0"
            elif (point1[0] - r <= mx <= point1[0] + r) and (point1[1] - r <= my <= point1[1] + r):
                dragging = "point1"

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        elif event.type == pygame.MOUSEMOTION and dragging:
            if dragging == "point0":
                point0[0], point0[1] = event.pos
            elif dragging == "point1":
                point1[0], point1[1] = event.pos

    bresenham(100, 100, 500, 300, screen, WHITE)
    draw()

    pygame.display.flip()

pygame.quit()