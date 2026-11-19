import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")
RES = 16
G_WIDTH = WIDTH // RES
G_HEIGHT = HEIGHT // RES

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

point0 = [400, 100]
point1 = [100, 300]
point2 = [500, 500]
point3 = [600, 200]
dragging = None
R = 50

def triangle(p0, p1, p2, color):
    v0, v1, v2 = p0, p1, p2
    if v0[1] > v1[1]:
        v0, v1 = v1, v0
    if v1[1] > v2[1]:
        v1, v2 = v2, v1
    if v0[1] > v1[1]:
        v0, v1 = v1, v0

    # Deltas
    dx_01 = v1[0] - v0[0]
    dy_01 = v1[1] - v0[1]
    dx_02 = v2[0] - v0[0]
    dy_02 = v2[1] - v0[1]
    dx_12 = v2[0] - v1[0]
    dy_12 = v2[1] - v1[1]

    # Slopes dx/dy
    step_01 = dx_01 / dy_01 if dy_01 != 0 else float('inf')
    step_02 = dx_02 / dy_02 if dy_02 != 0 else float('inf')
    step_12 = dx_12 / dy_12 if dy_12 != 0 else float('inf')

    x0, x1 = float(v0[0]), float(v0[0]) # could add 0.5 because pixel centers but pygame polygon doesnt do that so i wont
    short = step_01 > step_02 # 0 is left, 1 is right

    if v0[1] != v1[1]:
        for y in range(v0[1], v1[1]):
            for x in range(int(x0), int(x1)):
                pygame.draw.rect(screen, color, pygame.Rect(RES * x, RES * y, RES, RES)) # Fill in scanline
            if short:
                x0 += step_02 # Go the other way since the longer side is on the left
                x1 += step_01
            else:
                x0 += step_01
                x1 += step_02
    else: # If the top half is flat, set x1 to the rightmost point since it's not there yet
        x1 = float(v1[0])
        if x0 > x1: # Can be backwards since it's the same level it doesn't matter
            x0, x1 = x1, x0
            short = False
    
    if short: # Helps guarantee that the end point is at v1 so no floating point error happens before starting the bottom half
        x1 = float(v1[0])
    else:
        x0 = float(v1[0])

    if v1[1] != v2[1]:
        for y in range(v1[1], v2[1]):
            for x in range(int(x0), int(x1)):
                pygame.draw.rect(screen, color, pygame.Rect(RES * x, RES * y, RES, RES))
            if short:
                x0 += step_02
                x1 += step_12
            else:
                x0 += step_12
                x1 += step_02

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
            if (point0[0] - R <= mx <= point0[0] + R) and (point0[1] - R <= my <= point0[1] + R):
                dragging = "point0"
            elif (point1[0] - R <= mx <= point1[0] + R) and (point1[1] - R <= my <= point1[1] + R):
                dragging = "point1"
            elif (point2[0] - R <= mx <= point2[0] + R) and (point2[1] - R <= my <= point2[1] + R):
                dragging = "point2"
            elif (point3[0] - R <= mx <= point3[0] + R) and (point3[1] - R <= my <= point3[1] + R):
                dragging = "point3"

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        elif event.type == pygame.MOUSEMOTION and dragging:
            if dragging == "point0":
                point0[0], point0[1] = event.pos
            elif dragging == "point1":
                point1[0], point1[1] = event.pos
            elif dragging == "point2":
                point2[0], point2[1] = event.pos
            elif dragging == "point3":
                point3[0], point3[1] = event.pos

    p0 = (point0[0] // RES, point0[1] // RES)
    p1 = (point1[0] // RES, point1[1] // RES)
    p2 = (point2[0] // RES, point2[1] // RES)
    p3 = (point3[0] // RES, point3[1] // RES)
    #pygame.draw.polygon(screen, WHITE, [point0, point1, point2])
    #pygame.draw.polygon(screen, WHITE, [point0, point2, point3])
    triangle(p0, p1, p2, RED)
    triangle(p0, p2, p3, GREEN)
    #pygame.draw.circle(screen, WHITE, point0, R)
    #pygame.draw.circle(screen, WHITE, point1, R)
    #pygame.draw.circle(screen, WHITE, point2, R)

    pygame.display.flip()

pygame.quit()