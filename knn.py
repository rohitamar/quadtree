import numpy as np
import pygame
import math 
import heapq 

from quadtree import Rectangle, Quadtree, rects_and_pts

def distance(a: tuple, b: tuple) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
     
def circle_with_rect(cp: tuple, rad: float, rect: Rectangle) -> bool: 
    tl, w, h = rect.tl, rect.width, rect.height

    tr = (tl[0] + w, tl[1])
    bl = (tl[0], tl[1] + h)
    br = (tl[0] + w, tl[1] + h)

    # horizontal lines
    # tl --- tr, bl --- br 
    if rad ** 2 >= (cp[1] - tl[1]) ** 2:
        pm = math.sqrt(rad ** 2 - (cp[1] - tl[1]) ** 2) 
        if tl[0] <= cp[0] + pm <= tr[0] or tl[0] <= cp[0] - pm <= tr[0]:
            return True 
    
    if rad ** 2 >= (cp[1] - bl[1]) ** 2:
        pm = math.sqrt(rad ** 2 - (cp[1] - bl[1]) ** 2) 
        if bl[0] <= cp[0] + pm <= br[0] or bl[0] <= cp[0] - pm <= br[0]:
            return True 

    # vertical lines 
    # tl -- bl, tr --- br
    if rad ** 2 >= (cp[0] - tr[0]) ** 2:
        pm = math.sqrt(rad ** 2 - (cp[0] - tr[0]) ** 2) 
        if tr[1] <= cp[1] + pm <= br[1] or tr[1] <= cp[1] - pm <= br[1]:
            return True 

    if rad ** 2 >= (cp[0] - bl[0]) ** 2:
        pm = math.sqrt(rad ** 2 - (cp[0] - bl[0]) ** 2) 
        if tl[1] <= cp[1] + pm <= bl[1] or tl[1] <= cp[1] - pm <= bl[1]:
            return True 
    
    return distance(cp, tl) <= rad or distance(cp, tr) <= rad or distance(cp, bl) <= rad or distance(cp, br) <= rad 


def nearest_neighbor(root: Quadtree, pt: tuple, k: int) -> tuple:
    st = [root]
    hq = [(-1000000.0, (-1, -1))]
    while st:
        u = st.pop()
        if not u: continue
        if not u.divided:
            for p in u.arr:
                if p == pt: continue
                heapq.heappush(hq, (-distance(pt, p), p))
                if len(hq) > k:
                    heapq.heappop(hq)
        else:
            for qt in [u.ne, u.nw, u.se, u.sw]:
                d = -max(hq, key = lambda x : -x[0])[0]
                if circle_with_rect(pt, d, qt.bbox):
                    st.append(qt)

    hq = [(-x, y) for x, y in hq]
    hq.sort() 
    distances, pts = [h[0] for h in hq], [h[1] for h in hq]
    return distances, pts

def brute_nn(coords: list[tuple], pt: tuple, k: int) -> tuple:
    hq = [(-1000000.0, (-1, -1))]
    for coord in coords:
        if coord == pt: continue 
        heapq.heappush(hq, (-distance(coord, pt), coord))
        if len(hq) > k:
            heapq.heappop(hq)
    hq = [(-x, y) for x, y in hq]
    hq.sort() 
    distances, pts = [h[0] for h in hq], [h[1] for h in hq]
    return distances, pts 

# np.random.seed(6969)

height = 1600
width = 900
num_pts = 250
k = 15

q = Quadtree(Rectangle((1, 1), height, width), 3)

x = np.random.randint(low=1, high=height+1, size=num_pts)
y = np.random.randint(low=1, high=width+1, size=num_pts)

coords = [*zip(x, y)]

for coord in coords:
    q.insert(coord)

rects, pts = rects_and_pts(q)
_, knn_pts = nearest_neighbor(q, coords[0], k)
_, brute_pts = brute_nn(coords, coords[0], k)

print(coords[0])
print(knn_pts)
print(brute_pts)

print(brute_pts == knn_pts)

pygame.init()

screen = pygame.display.set_mode((height, width))
dot_color = (255, 0, 0)
rect_color = (255, 255, 255)
knn_color = (0, 0, 255)
point_color = (0, 255, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    for r in rects:
        pygame.draw.rect(screen, rect_color, r, 1)
    
    for p in pts:
        pygame.draw.circle(screen, dot_color, p, 4)
    
    for p in knn_pts:
        pygame.draw.circle(screen, knn_color, p, 4)

    pygame.draw.circle(screen, point_color, coords[0], 4)
    pygame.display.flip()


