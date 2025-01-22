import numpy as np

from quadtree import Point, Rectangle, Quadtree

# np.random_seed(6969)

r = Rectangle(Point(1, 1), Point(101, 101))
q = Quadtree(r, 3)

x = np.random.randint(low=1, high=102, size=30)
y = np.random.randint(low=1, high=102, size=30)

coords = [Point(a, b) for a, b in zip(x, y)]
for coord in coords:
    q.insert(coord)

import pygame
 
# Initializing Pygame
pygame.init()
 
# Initializing surface
surface = pygame.display.set_mode((400,300))
 
# Initializing Color
color = (255,0,0)
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.draw.rect(surface, color, pygame.Rect(30, 30, 100, 10))
    pygame.display.flip()

