import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")

SPEED = 0.05
ROTATION_SPEED = math.radians(2)
POS_X = 0.5
POS_Y = 3.5
ANGLE = 0
FOV = math.radians(60)
TOTAL_RAYS = 400
MAX_DISTANCE = 10

world_map = [
    [0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0]
]

def cast_ray(angle, pos):
    x, y = POS_X, POS_Y
    distance = 0
    hit = False
    side = None # 0 = vertical wall, 1 = horizontal wall

    # Ray direction
    dx = math.cos(angle)
    dy = math.sin(angle)

    # Calculate initial distances to next grid intersections
    delta_dist_x = abs(1 / dx) if dx != 0 else float('inf') # Since it's infinity it will never be shorter so we will never
    delta_dist_y = abs(1 / dy) if dy != 0 else float('inf') # move on the x axis (makes sense if you're facing towards y)

    # Distance to first x axis
    if dx > 0:
        step_x = 1
        side_dist_x = (math.ceil(x) - x) * delta_dist_x # Going right so ceil is nearer
    else:
        step_x = -1
        side_dist_x = (x - math.floor(x)) * delta_dist_x # Going left so floor is nearer, also backwards because direction is negative

    # Distance to first y axis
    if dy > 0:
        step_y = 1
        side_dist_y = (math.ceil(y) - y) * delta_dist_y # Going up so ceil is nearer
    else:
        step_y = -1
        side_dist_y = (y - math.floor(y)) * delta_dist_y # Going down so floor is nearer, also backwards because direction is negative

    # DDA loop
    while not hit and distance < MAX_DISTANCE:
        if side_dist_x < side_dist_y: # Change is done after setting distance so that we can compare the new distance before applying it
            distance = side_dist_x # Distance so far
            side_dist_x += delta_dist_x # Increment distance to next x axis
            x += step_x # Move to next grid because we crossed the x axis

            side = 0  # Vertical wall
        else:
            distance = side_dist_y # Distance so far
            side_dist_y += delta_dist_y # Increment distance to next y axis
            y += step_y # Move to next grid because we crossed the y axis

            side = 1  # Horizontal wall

        # Repeat world map
        if world_map[int(abs(y % 5))][int(abs(x % 5))] == 1:
            hit = True

    if hit:
        corrected_distance = distance * math.cos(angle - ANGLE)

        height = 250 / corrected_distance
        color = min(max(255 / corrected_distance, 0), 255) if side == 0 else min(max((255 / corrected_distance) * 0.6, 0), 255) # Darken vertical walls

        pygame.draw.line(screen, (color, color, color),
                         (pos, HEIGHT / 2 + height),
                         (pos, HEIGHT / 2 - height),
                         int(WIDTH / TOTAL_RAYS))
        


def raycast_scene():
    ray_direction = ANGLE - FOV / 2
    screen_position = 0

    for ray in range(TOTAL_RAYS):
        cast_ray(ray_direction, screen_position)

        ray_direction = ANGLE - FOV / 2 + FOV / TOTAL_RAYS * ray
        screen_position += WIDTH / TOTAL_RAYS

running = True
while running:
    screen.fill((0, 0, 0))
    dt = clock.tick(60) / 1000
    print(clock.get_fps())
    
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