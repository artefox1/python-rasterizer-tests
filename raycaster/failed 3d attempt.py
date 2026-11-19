import math
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")

SPEED = 0.05
ROTATION_SPEED = math.radians(2)
POS_X = 0
POS_Y = 0
POS_Z = 0
ROT_X = 0
ROT_Y = 0
RES = 8
MAX_DISTANCE = 10

world = {}
world[(0, 0, -1)] = 1
world[(1, 1, -2)] = 1
world[(1, 2, -2)] = 1

def cast_ray(ray_x, ray_y, ray_z, u, v):
    x, y, z = POS_X, POS_Y, POS_Z
    distance = 0
    hit = False

    # Calculate initial distances to next grid intersections
    delta_dist_x = abs(1 / ray_x) if ray_x != 0 else float('inf')
    delta_dist_y = abs(1 / ray_y) if ray_y != 0 else float('inf')
    delta_dist_z = abs(1 / ray_z) if ray_z != 0 else float('inf')

    # Distance to first x axis
    if ray_x > 0:
        step_x = 1
        side_dist_x = (math.ceil(x) - x) * delta_dist_x
    else:
        step_x = -1
        side_dist_x = (x - math.floor(x)) * delta_dist_x

    # Distance to first y axis
    if ray_y > 0:
        step_y = 1
        side_dist_y = (math.ceil(y) - y) * delta_dist_y
    else:
        step_y = -1
        side_dist_y = (y - math.floor(y)) * delta_dist_y

    # Distance to first z axis
    if ray_z > 0:
        step_z = 1
        side_dist_z = (math.ceil(z) - z) * delta_dist_z
    else:
        step_z = -1
        side_dist_z = (z - math.floor(z)) * delta_dist_z

    # DDA loop
    while not hit and distance < MAX_DISTANCE:
        if side_dist_x < side_dist_y:
            distance = side_dist_x
            side_dist_x += delta_dist_x
            x += step_x
        elif side_dist_y < side_dist_z:
            distance = side_dist_y
            side_dist_y += delta_dist_y
            y += step_y
        else:
            distance = side_dist_z
            side_dist_z += delta_dist_z
            z += step_z

        if world.get((math.floor(x), math.floor(y), math.floor(z)), 0) == 1:
            hit = True

    if hit:
        pygame.Surface.set_at(screen, (u * RES, HEIGHT - v * RES), (255, 255, 255))


def raycast_scene():
    x = 0
    y = 0
    
    x_inc = 1 / (WIDTH // RES)
    y_inc = 1 / (HEIGHT // RES)

    for u in range(HEIGHT // RES):
        for v in range(WIDTH // RES):
            ray_x = 2 * x - 1
            ray_y = 2 * y - 1
            ray_z = -1

            ray_length = math.sqrt(ray_x ** 2 + ray_y ** 2 + ray_z ** 2)

            ray_x /= ray_length
            ray_y /= ray_length
            ray_z /= ray_length

            cast_ray(ray_x, ray_y, ray_z, u, v)
            x += x_inc
        y += y_inc
        

running = True
while running:
    screen.fill((0, 0, 0))
    dt = clock.tick(60) / 1000
    delta = dt * 60
    print(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        POS_Z -= SPEED * delta
    if keys[pygame.K_s]:
        POS_Z += SPEED * delta
    if keys[pygame.K_a]:
        POS_X -= SPEED * delta
    if keys[pygame.K_d]:
        POS_X += SPEED * delta
    if keys[pygame.K_e]:
        POS_Y += SPEED * delta
    if keys[pygame.K_q]:
        POS_Y -= SPEED * delta
    

    raycast_scene()
    pygame.display.flip()

pygame.quit()