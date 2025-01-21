class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
class Rectangle:
    def __init__(self, tl, tr, bl, br):
        # tl = topleft, tr = topright, bl = bottomleft,  br = bottomright
        self.tl = tl
        self.tr = tr
        self.bl = bl 
        self.br = br 

    def __contains__(self, p):
        mn_x, mx_x = min(tl.x, tr.x), max(tl.x, tr.x)
        mn_y, mx_y = min(tl.y, tr.y), max(tl.y, tr.y)

        return mn_x <= p.x <= mx_x and mn_y <= p.y <= mx_y
    
    def __repr__(self):
        

class Quadtree:
    def __init__(self):
