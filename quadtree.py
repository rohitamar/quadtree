class Rectangle:
    def __init__(self, tl: tuple, width: float, height: float):
        # tl = top left, width, height
        self.tl: tuple = tl 
        self.width: int = width 
        self.height: int = height 

    def __contains__(self, p: tuple) -> bool:
        return self.tl[0] <= p[0] <= self.tl[0] + self.width and self.tl[1] <= p[1] <= self.tl[1] + self.height 

    def pyg(self) -> tuple:
        return *self.tl, self.width, self.height
    
class Quadtree:
    def __init__(self, bbox: Rectangle, size: int):
        self.size: int = size
        self.bbox: Rectangle = bbox 
        self.arr: list[tuple] = []
        self.divided: bool = False 

        self.ne: Quadtree = None
        self.nw: Quadtree = None 
        self.se: Quadtree = None 
        self.sw: Quadtree = None  

    def insert(self, p: tuple) -> bool:
        if p not in self.bbox:
            return False

        if len(self.arr) < self.size:
            self.arr.append(p)
            return
        
        self.divided = True 
        bl = self.bbox.tl 
        w = self.bbox.width 
        h = self.bbox.height 

        self.ne = Quadtree(Rectangle((bl[0] + w / 2, bl[1]), w / 2, h / 2), self.size)
        self.se = Quadtree(Rectangle((bl[0] + w / 2, bl[1] + h / 2), w / 2, h / 2), self.size) 
        self.nw = Quadtree(Rectangle(bl, w / 2, h / 2), self.size)
        self.sw = Quadtree(Rectangle((bl[0], bl[1] + h / 2), w / 2, h / 2), self.size)

        self.arr.append(p)
        for p in self.arr:
            for qt in [self.ne, self.se, self.nw, self.sw]:
                if qt.insert(p):
                    break
        return True 
            
def rects_and_pts(root: Quadtree):
    st, pts, rects = [root], [], []
    while st:
        u = st.pop()
        if not u: continue 
        rects.append(u.bbox.pyg())
        if not u.divided:
            for p in u.arr:
                pts.append(p)
        else:
            st.extend([u.ne, u.nw, u.se, u.sw])

    return rects, pts
    



            
    


        
