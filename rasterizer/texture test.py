import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("shut the fuck up")

texture = pygame.image.load("rasterizer/cobblestone.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def render():
    for y in range(16):
        for x in range(16):
            screen.set_at((x, y), texture.get_at((x, y)))

running = True
while running:
    screen.fill(BLACK)
    dt = clock.tick(60) / 1000
    print(clock.get_fps())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    render()
    pygame.display.flip()

pygame.quit()