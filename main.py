import numpy as np
from quadtree import Point, Rectangle

r = Rectangle((1, 1), (101, 101))
q = Quadtree(r, 3)

q.insert(Point(10, 13))
