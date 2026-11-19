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
ASPECT = WIDTH / HEIGHT

texture0 = pygame.image.load("cobblestone.png")
texture1 = pygame.image.load("oak_planks.png")
T_WIDTH, T_HEIGHT = texture0.get_size()

depth_buffer = [[-float('inf') for _ in range(G_WIDTH)] for _ in range(G_HEIGHT)]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# X, Y, Z, U, V
point0 = [-1, -1, -1, 0, 0]
point1 = [-1, 1, -1, 0, 1]
point2 = [1, -1, -1, 1, 0]
point3 = [1, 1, -1, 1, 1]
point4 = [-1, -1, 1, 0, 0]
point5 = [-1, 1, 1, 0, 1]
point6 = [1, -1, 1, 1, 0]
point7 = [1, 1, 1, 1, 1]

def triangle(t0, t1, t2, texture):
    p0, p1, p2 = t0, t1, t2
    if p0[1] > p1[1]:
        p0, p1 = p1, p0
    if p1[1] > p2[1]:
        p1, p2 = p2, p1
    if p0[1] > p1[1]:
        p0, p1 = p1, p0

    # Perspective correction (u / z, v / z)
    p0[3] = p0[3] / p0[2] if p0[2] != 0 else float('inf')
    p0[4] = p0[4] / p0[2] if p0[2] != 0 else float('inf')
    p1[3] = p1[3] / p1[2] if p1[2] != 0 else float('inf')
    p1[4] = p1[4] / p1[2] if p1[2] != 0 else float('inf')
    p2[3] = p2[3] / p2[2] if p2[2] != 0 else float('inf')
    p2[4] = p2[4] / p2[2] if p2[2] != 0 else float('inf')

    # z = 1 / z
    p0[2] = 1 / p0[2] if p0[2] != 0 else float('inf')
    p1[2] = 1 / p1[2] if p1[2] != 0 else float('inf')
    p2[2] = 1 / p2[2] if p2[2] != 0 else float('inf')

    # Deltas
    dx_01 = p1[0] - p0[0]
    dy_01 = p1[1] - p0[1]
    dx_02 = p2[0] - p0[0]
    dy_02 = p2[1] - p0[1]
    dx_12 = p2[0] - p1[0]
    dy_12 = p2[1] - p1[1]

    # Deltas for attributes
    dz_01 = p1[2] - p0[2]
    du_01 = p1[3] - p0[3]
    dv_01 = p1[4] - p0[4]
    dz_02 = p2[2] - p0[2]
    du_02 = p2[3] - p0[3]
    dv_02 = p2[4] - p0[4]
    dz_12 = p2[2] - p1[2]
    du_12 = p2[3] - p1[3]
    dv_12 = p2[4] - p1[4]

    # Slopes dx/dy
    step_01 = dx_01 / dy_01 if dy_01 != 0 else float('inf')
    step_02 = dx_02 / dy_02 if dy_02 != 0 else float('inf')
    step_12 = dx_12 / dy_12 if dy_12 != 0 else float('inf')

    # Slopes for attributes
    step_z_01 = dz_01 / dy_01 if dy_01 != 0 else 0
    step_u_01 = du_01 / dy_01 if dy_01 != 0 else 0
    step_v_01 = dv_01 / dy_01 if dy_01 != 0 else 0
    step_z_02 = dz_02 / dy_02 if dy_02 != 0 else 0
    step_u_02 = du_02 / dy_02 if dy_02 != 0 else 0
    step_v_02 = dv_02 / dy_02 if dy_02 != 0 else 0
    step_z_12 = dz_12 / dy_12 if dy_12 != 0 else 0
    step_u_12 = du_12 / dy_12 if dy_12 != 0 else 0
    step_v_12 = dv_12 / dy_12 if dy_12 != 0 else 0

    x0, x1 = float(p0[0]), float(p0[0])
    z0, u0, v0, z1, u1, v1 = float(p0[2]), float(p0[3]), float(p0[4]), float(p0[2]), float(p0[3]), float(p0[4])
    short = step_01 > step_02 # 0 is left, 1 is right

    if p0[1] != p1[1]:
        for y in range(p0[1], p1[1]):
            x_step_z = (z1 - z0) / (x1 - x0) if x1 != x0 else 0
            x_step_u = (u1 - u0) / (x1 - x0) if x1 != x0 else 0
            x_step_v = (v1 - v0) / (x1 - x0) if x1 != x0 else 0
            z = z0
            u = u0
            v = v0

            for x in range(int(x0), int(x1)):
                uu = int(min(max((u / z) * T_WIDTH, 0), T_WIDTH - 1))
                vv = int(min(max((v / z) * T_HEIGHT, 0), T_HEIGHT - 1))
                if 0 <= y < G_HEIGHT and 0 <= x < G_WIDTH:
                    if z > depth_buffer[y][x]: # backwards because interpolate 1/z
                        depth_buffer[y][x] = z
                        pygame.draw.rect(screen, texture.get_at((uu, vv)), pygame.Rect(RES * x, RES * y, RES, RES))
                z += x_step_z
                u += x_step_u
                v += x_step_v
            if short:
                x0 += step_02
                x1 += step_01

                z0 += step_z_02
                u0 += step_u_02
                v0 += step_v_02
                z1 += step_z_01
                u1 += step_u_01
                v1 += step_v_01
            else:
                x0 += step_01
                x1 += step_02

                z0 += step_z_01
                u0 += step_u_01
                v0 += step_v_01
                z1 += step_z_02
                u1 += step_u_02
                v1 += step_v_02
    else:
        x1 = float(p1[0])
        z1 = float(p1[2])
        u1 = float(p1[3])
        v1 = float(p1[4])
        if x0 > x1:
            x0, x1 = x1, x0
            z0, z1 = z1, z0
            u0, u1 = u1, u0
            v0, v1 = v1, v0
            short = False
    
    if short:
        x1 = float(p1[0])
    else:
        x0 = float(p1[0])

    if p1[1] != p2[1]:
        for y in range(p1[1], p2[1]):
            x_step_z = (z1 - z0) / (x1 - x0) if x1 != x0 else 0
            x_step_u = (u1 - u0) / (x1 - x0) if x1 != x0 else 0
            x_step_v = (v1 - v0) / (x1 - x0) if x1 != x0 else 0
            z = z0
            u = u0
            v = v0

            for x in range(int(x0), int(x1)):
                uu = int(min(max((u / z) * T_WIDTH, 0), T_WIDTH - 1))
                vv = int(min(max((v / z) * T_HEIGHT, 0), T_HEIGHT - 1))
                if 0 <= y < G_HEIGHT and 0 <= x < G_WIDTH:
                    if z > depth_buffer[y][x]: # backwards because interpolate 1/z
                        depth_buffer[y][x] = z
                        pygame.draw.rect(screen, texture.get_at((uu, vv)), pygame.Rect(RES * x, RES * y, RES, RES))
                z += x_step_z
                u += x_step_u
                v += x_step_v
            if short:
                x0 += step_02
                x1 += step_12

                z0 += step_z_02
                u0 += step_u_02
                v0 += step_v_02
                z1 += step_z_12
                u1 += step_u_12
                v1 += step_v_12
            else:
                x0 += step_12
                x1 += step_02

                z0 += step_z_12
                u0 += step_u_12
                v0 += step_v_12
                z1 += step_z_02
                u1 += step_u_02
                v1 += step_v_02

def scale(x, y, z, sx, sy, sz):
    x_new = x * sx
    y_new = y * sy
    z_new = z * sz
    return x_new, y_new, z_new

def rotate_x(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    y_new = y * cos_a - z * sin_a
    z_new = y * sin_a + z * cos_a
    return x, y_new, z_new

def rotate_y(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x_new = x * cos_a + z * sin_a
    z_new = -x * sin_a + z * cos_a
    return x_new, y, z_new

def rotate_z(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x_new = x * cos_a - y * sin_a
    y_new = x * sin_a + y * cos_a
    return x_new, y_new, z

def translate(x, y, z, dx, dy, dz):
    x_new = x + dx
    y_new = y + dy
    z_new = z + dz
    return x_new, y_new, z_new

def projection(x, y, z, focal):
    x_new = x * focal / z / ASPECT
    y_new = y * focal / z
    return x_new, y_new # want to preserve z value for depth

running = True
while running:
    screen.fill(BLACK)
    for y in range(G_HEIGHT):
        for x in range(G_WIDTH):
            depth_buffer[y][x] = -float('inf')

    dt = clock.tick(60) / 1000
    ms = pygame.time.get_ticks()
    print(clock.get_fps())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angle0 = math.radians(ms / 1000 * 360 * 0.1)
    angle1 = math.radians(ms / 1000 * 180 * 0.1)
    dist = 4
    p0 = point0[:]
    p1 = point1[:]
    p2 = point2[:]
    p3 = point3[:]
    p4 = point4[:]
    p5 = point5[:]
    p6 = point6[:]
    p7 = point7[:]
    p0[0], p0[1], p0[2] = rotate_y(point0[0], point0[1], point0[2], angle0)
    p1[0], p1[1], p1[2] = rotate_y(point1[0], point1[1], point1[2], angle0)
    p2[0], p2[1], p2[2] = rotate_y(point2[0], point2[1], point2[2], angle0)
    p3[0], p3[1], p3[2] = rotate_y(point3[0], point3[1], point3[2], angle0)
    p4[0], p4[1], p4[2] = rotate_y(point4[0], point4[1], point4[2], angle0)
    p5[0], p5[1], p5[2] = rotate_y(point5[0], point5[1], point5[2], angle0)
    p6[0], p6[1], p6[2] = rotate_y(point6[0], point6[1], point6[2], angle0)
    p7[0], p7[1], p7[2] = rotate_y(point7[0], point7[1], point7[2], angle0)
    p0[0], p0[1], p0[2] = rotate_z(p0[0], p0[1], p0[2], angle1)
    p1[0], p1[1], p1[2] = rotate_z(p1[0], p1[1], p1[2], angle1)
    p2[0], p2[1], p2[2] = rotate_z(p2[0], p2[1], p2[2], angle1)
    p3[0], p3[1], p3[2] = rotate_z(p3[0], p3[1], p3[2], angle1)
    p4[0], p4[1], p4[2] = rotate_z(p4[0], p4[1], p4[2], angle1)
    p5[0], p5[1], p5[2] = rotate_z(p5[0], p5[1], p5[2], angle1)
    p6[0], p6[1], p6[2] = rotate_z(p6[0], p6[1], p6[2], angle1)
    p7[0], p7[1], p7[2] = rotate_z(p7[0], p7[1], p7[2], angle1)
    p0[0], p0[1], p0[2] = translate(p0[0], p0[1], p0[2], 0, 0, dist)
    p1[0], p1[1], p1[2] = translate(p1[0], p1[1], p1[2], 0, 0, dist)
    p2[0], p2[1], p2[2] = translate(p2[0], p2[1], p2[2], 0, 0, dist)
    p3[0], p3[1], p3[2] = translate(p3[0], p3[1], p3[2], 0, 0, dist)
    p4[0], p4[1], p4[2] = translate(p4[0], p4[1], p4[2], 0, 0, dist)
    p5[0], p5[1], p5[2] = translate(p5[0], p5[1], p5[2], 0, 0, dist)
    p6[0], p6[1], p6[2] = translate(p6[0], p6[1], p6[2], 0, 0, dist)
    p7[0], p7[1], p7[2] = translate(p7[0], p7[1], p7[2], 0, 0, dist)
    p0[0], p0[1] = projection(p0[0], p0[1], p0[2], 1)
    p1[0], p1[1] = projection(p1[0], p1[1], p1[2], 1)
    p2[0], p2[1] = projection(p2[0], p2[1], p2[2], 1)
    p3[0], p3[1] = projection(p3[0], p3[1], p3[2], 1)
    p4[0], p4[1] = projection(p4[0], p4[1], p4[2], 1)
    p5[0], p5[1] = projection(p5[0], p5[1], p5[2], 1)
    p6[0], p6[1] = projection(p6[0], p6[1], p6[2], 1)
    p7[0], p7[1] = projection(p7[0], p7[1], p7[2], 1)
    p0[0] = int((p0[0] + 1) / 2 * G_WIDTH)
    p0[1] = int((p0[1] + 1) / 2 * G_HEIGHT)
    p1[0] = int((p1[0] + 1) / 2 * G_WIDTH)
    p1[1] = int((p1[1] + 1) / 2 * G_HEIGHT)
    p2[0] = int((p2[0] + 1) / 2 * G_WIDTH)
    p2[1] = int((p2[1] + 1) / 2 * G_HEIGHT)
    p3[0] = int((p3[0] + 1) / 2 * G_WIDTH)
    p3[1] = int((p3[1] + 1) / 2 * G_HEIGHT)
    p4[0] = int((p4[0] + 1) / 2 * G_WIDTH)
    p4[1] = int((p4[1] + 1) / 2 * G_HEIGHT)
    p5[0] = int((p5[0] + 1) / 2 * G_WIDTH)
    p5[1] = int((p5[1] + 1) / 2 * G_HEIGHT)
    p6[0] = int((p6[0] + 1) / 2 * G_WIDTH)
    p6[1] = int((p6[1] + 1) / 2 * G_HEIGHT)
    p7[0] = int((p7[0] + 1) / 2 * G_WIDTH)
    p7[1] = int((p7[1] + 1) / 2 * G_HEIGHT)
    triangle(p0[:], p1[:], p2[:], texture0)
    triangle(p1[:], p2[:], p3[:], texture0)
    triangle(p4[:], p5[:], p6[:], texture1)
    triangle(p5[:], p6[:], p7[:], texture1)

    pygame.display.flip()

pygame.quit()