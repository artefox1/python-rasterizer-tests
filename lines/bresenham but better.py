import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")
RES = 8
G_WIDTH = WIDTH // RES
G_HEIGHT = HEIGHT // RES

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

point0 = [50, 50]
point1 = [500, 500]
dragging = None
R = 50

def bresenham(x0, y0, x1, y1, color):

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1

    if dy > dx:
        dx, dy = dy, dx
        steep = True
    else:
        steep = False

    x, y = x0, y0
    p = 2 * dy - dx
    for i in range(dx + 1):
        pygame.draw.rect(screen, color, pygame.Rect(RES * x, RES * y, RES, RES))

        if p > 0:
            if steep:
                x += sx
            else:
                y += sy
            p -= 2 * dx
        if steep:
            y += sy
        else:
            x += sx
        p += 2 * dy

running = True
while running:
    screen.fill(BLACK)
    dt = clock.tick(60) / 1000
    print(clock.get_fps())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos # Get mouse position
            if (point0[0] - R <= mx <= point0[0] + R) and (point0[1] - R <= my <= point0[1] + R): # If inside radius, set dragging to point0
                dragging = "point0"
            elif (point1[0] - R <= mx <= point1[0] + R) and (point1[1] - R <= my <= point1[1] + R): # If inside radius, set dragging to point1
                dragging = "point1"

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        elif event.type == pygame.MOUSEMOTION and dragging:
            if dragging == "point0":
                point0[0], point0[1] = event.pos # While dragging point0, set point0 to mouse position
            elif dragging == "point1":
                point1[0], point1[1] = event.pos # While dragging point1, set point1 to mouse position

    bresenham(100 // RES, 100 // RES, 500 // RES, 300 // RES, WHITE)
    bresenham(point0[0] // RES, point0[1] // RES, point1[0] // RES, point1[1] // RES, RED)
    #pygame.draw.circle(screen, WHITE, point0, R)
    #pygame.draw.circle(screen, WHITE, point1, R)

    pygame.display.flip()

pygame.quit()