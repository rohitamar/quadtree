import numpy as np
import pygame
from quadtree import Rectangle, Quadtree

# np.random.seed(6969)

height = 1200
width = 900
num_pts = 90

q = Quadtree(Rectangle((1, 1), 1200, 900), 3)

x = np.random.randint(low=1, high=height+1, size=num_pts)
y = np.random.randint(low=1, high=width+1, size=num_pts)

for coord in [*zip(x, y)]:
    q.insert(coord)

st = [q]
pts, rects = [], []

while st:
    u = st.pop()
    if not u: continue 
    rects.append(u.bbox.pyg())
    if not u.divided:
        for p in u.arr:
            pts.append((p[0], p[1]))
    else:
        st.extend([u.ne, u.nw, u.se, u.sw])

pygame.init()

screen = pygame.display.set_mode((1200, 900))
dot_color = (255, 0, 0)
rect_color = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for r in rects:
        pygame.draw.rect(screen, rect_color, r, 1)
    
    for p in pts:
        pygame.draw.circle(screen, dot_color, p, 2)
    
    pygame.display.flip()


