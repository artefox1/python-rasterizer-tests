import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")
RES = 4
G_WIDTH = WIDTH // RES
G_HEIGHT = HEIGHT // RES

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# X, Y, R, G, B
point0 = [400, 100, 255, 0, 0]
point1 = [100, 300, 0, 255, 0]
point2 = [500, 500, 0, 0, 255]
point3 = [600, 200, 255, 255, 0]
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

    # Deltas for colors
    dr_01 = v1[2] - v0[2]
    dg_01 = v1[3] - v0[3]
    db_01 = v1[4] - v0[4]
    dr_02 = v2[2] - v0[2]
    dg_02 = v2[3] - v0[3]
    db_02 = v2[4] - v0[4]
    dr_12 = v2[2] - v1[2]
    dg_12 = v2[3] - v1[3]
    db_12 = v2[4] - v1[4]

    # Slopes dx/dy
    step_01 = dx_01 / dy_01 if dy_01 != 0 else float('inf')
    step_02 = dx_02 / dy_02 if dy_02 != 0 else float('inf')
    step_12 = dx_12 / dy_12 if dy_12 != 0 else float('inf')

    # Slopes for colors
    step_r_01 = dr_01 / dy_01 if dy_01 != 0 else 0
    step_g_01 = dg_01 / dy_01 if dy_01 != 0 else 0
    step_b_01 = db_01 / dy_01 if dy_01 != 0 else 0
    step_r_02 = dr_02 / dy_02 if dy_02 != 0 else 0
    step_g_02 = dg_02 / dy_02 if dy_02 != 0 else 0
    step_b_02 = db_02 / dy_02 if dy_02 != 0 else 0
    step_r_12 = dr_12 / dy_12 if dy_12 != 0 else 0
    step_g_12 = dg_12 / dy_12 if dy_12 != 0 else 0
    step_b_12 = db_12 / dy_12 if dy_12 != 0 else 0

    x0, x1 = float(v0[0]), float(v0[0])
    r0, g0, b0, r1, g1, b1 = float(v0[2]), float(v0[3]), float(v0[4]), float(v0[2]), float(v0[3]), float(v0[4])
    short = step_01 > step_02 # 0 is left, 1 is right

    if v0[1] != v1[1]:
        for y in range(v0[1], v1[1]):
            x_step_r = (r1 - r0) / (x1 - x0) if x1 != x0 else 0
            x_step_g = (g1 - g0) / (x1 - x0) if x1 != x0 else 0
            x_step_b = (b1 - b0) / (x1 - x0) if x1 != x0 else 0
            r = r0
            g = g0
            b = b0

            for x in range(int(x0), int(x1)):
                pygame.draw.rect(screen, (r, g, b), pygame.Rect(RES * x, RES * y, RES, RES))
                r += x_step_r
                g += x_step_g
                b += x_step_b
            if short:
                x0 += step_02
                x1 += step_01

                r0 += step_r_02
                g0 += step_g_02
                b0 += step_b_02
                r1 += step_r_01
                g1 += step_g_01
                b1 += step_b_01
            else:
                x0 += step_01
                x1 += step_02

                r0 += step_r_01
                g0 += step_g_01
                b0 += step_b_01
                r1 += step_r_02
                g1 += step_g_02
                b1 += step_b_02
    else:
        x1 = float(v1[0])
        r1 = float(v1[2])
        g1 = float(v1[3])
        b1 = float(v1[4])
        if x0 > x1:
            x0, x1 = x1, x0
            r0, r1 = r1, r0
            g0, g1 = g1, g0
            b0, b1 = b1, b0
            short = False
    
    if short:
        x1 = float(v1[0])
    else:
        x0 = float(v1[0])

    if v1[1] != v2[1]:
        for y in range(v1[1], v2[1]):
            x_step_r = (r1 - r0) / (x1 - x0) if x1 != x0 else 0
            x_step_g = (g1 - g0) / (x1 - x0) if x1 != x0 else 0
            x_step_b = (b1 - b0) / (x1 - x0) if x1 != x0 else 0
            r = r0
            g = g0
            b = b0

            for x in range(int(x0), int(x1)):
                pygame.draw.rect(screen, (r, g, b), pygame.Rect(RES * x, RES * y, RES, RES))
                r += x_step_r
                g += x_step_g
                b += x_step_b
            if short:
                x0 += step_02
                x1 += step_12

                r0 += step_r_02
                g0 += step_g_02
                b0 += step_b_02
                r1 += step_r_12
                g1 += step_g_12
                b1 += step_b_12
            else:
                x0 += step_12
                x1 += step_02

                r0 += step_r_12
                g0 += step_g_12
                b0 += step_b_12
                r1 += step_r_02
                g1 += step_g_02
                b1 += step_b_02

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

    p0 = (point0[0] // RES, point0[1] // RES, point0[2], point0[3], point0[4])
    p1 = (point1[0] // RES, point1[1] // RES, point1[2], point1[3], point1[4])
    p2 = (point2[0] // RES, point2[1] // RES, point2[2], point2[3], point2[4])
    p3 = (point3[0] // RES, point3[1] // RES, point3[2], point3[3], point3[4])
    #pygame.draw.polygon(screen, WHITE, [point0, point1, point2])
    #pygame.draw.polygon(screen, WHITE, [point0, point2, point3])
    triangle(p0, p1, p2, RED)
    #triangle(p0, p2, p3, GREEN)
    #pygame.draw.circle(screen, WHITE, point0, R)
    #pygame.draw.circle(screen, WHITE, point1, R)
    #pygame.draw.circle(screen, WHITE, point2, R)

    pygame.display.flip()

pygame.quit()