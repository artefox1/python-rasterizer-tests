import math
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")

SPEED = 0.05
ROTATION_SPEED = math.radians(2)
POS_X = 0.5
POS_Y = 3.5
ANGLE = 0
FOV = math.radians(60)
TOTAL_RAYS = 600
DISTANCE_INCREMENT = 0.005
MAX_DISTANCE = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

world_map = [
    [0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0]
]

def cast_ray(angle, pos):
    x, y = POS_X, POS_Y

    cos_angle = DISTANCE_INCREMENT * math.cos(angle)
    sin_angle = DISTANCE_INCREMENT * math.sin(angle)
    distance = 0

    while distance < MAX_DISTANCE:
        x += cos_angle
        y += sin_angle
        distance += DISTANCE_INCREMENT

        if 0 <= int(x) < len(world_map[0]) and 0 <= int(y) < len(world_map):
            if world_map[int(x)][int(y)] == 1:
                corrected = distance * math.cos(angle - ANGLE)
                height = 250 / corrected
                c = min(255 / corrected, 255)

                pygame.draw.line(screen, (c, c, c),
                        (pos, HEIGHT / 2 + height),
                        (pos, HEIGHT / 2 - height),
                        int(WIDTH / TOTAL_RAYS)
                )
                return
    return
        


def raycast_scene():
    ray_direction = ANGLE - FOV / 2
    screen_position = 0

    for ray in range(TOTAL_RAYS):
        cast_ray(ray_direction, screen_position)

        ray_direction += FOV / TOTAL_RAYS
        screen_position += WIDTH / TOTAL_RAYS

running = True
while running:
    screen.fill(BLACK)
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ANGLE -= ROTATION_SPEED * dt * 60
    if keys[pygame.K_RIGHT]:
        ANGLE += ROTATION_SPEED * dt * 60
    if keys[pygame.K_w]:
        POS_X += math.cos(ANGLE) * SPEED * dt * 60
        POS_Y += math.sin(ANGLE) * SPEED * dt * 60
    if keys[pygame.K_s]:
        POS_X -= math.cos(ANGLE) * SPEED * dt * 60
        POS_Y -= math.sin(ANGLE) * SPEED * dt * 60
    if keys[pygame.K_a]:
        POS_X += math.sin(ANGLE) * SPEED * dt * 60
        POS_Y -= math.cos(ANGLE) * SPEED * dt * 60
    if keys[pygame.K_d]:
        POS_X -= math.sin(ANGLE) * SPEED * dt * 60
        POS_Y += math.cos(ANGLE) * SPEED * dt * 60
    

    raycast_scene()
    pygame.display.flip()

pygame.quit()