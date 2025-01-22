class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

class Rectangle:
    def __init__(self, bl: Point, tr: Point):
        if not isinstance(bl, Point):
            raise TypeError(f"Input must be of type Point, but given {type(bl).__name__}")
        
        if not isinstance(tr, Point):
            raise TypeErorr(f"Input must of type Point, but given {type(tr).__name__}")

        # bl = bottom left, tr = top right
        self.bl: Point = bl 
        self.tr: Point = tr 

    def __contains__(self, p: Point) -> bool:
        if not isinstance(p, Point):
            raise TypeError(f"Input must of type Point, but given {type(p).__name__}")
        mn_x, mx_x = min(self.bl.x, self.tr.x), max(self.bl.x, self.tr.x)
        mn_y, mx_y = min(self.bl.y, self.tr.y), max(self.bl.y, self.tr.y)

        return mn_x <= p.x <= mx_x and mn_y <= p.y <= mx_y
    
    def midpoint(self) -> Point:
        return Point((self.bl.x + self.tr.x) / 2, (self.bl.y + self.tr.y) / 2)

    def __repr__(self) -> str:
        return f"Rectangle(bl: {self.bl} tr: {self.tr})" 
    
    def points() -> List[Point]:
        return [self.bl, Point(bl.x, tr.y), self.tr, Point(tr.x, bl.y)]

class Quadtree:
    def __init__(self, bbox: Rectangle, size: int):
        self.size: int = size
        self.bbox: Rectangle = bbox 
        self.arr: List[Point] = []
        self.divided: bool = False 

        self.ne: Quadtree = None
        self.nw: Quadtree = None 
        self.se: Quadtree = None 
        self.sw: Quadtree = None  

    def insert(self, p) -> bool:
        if not isinstance(p, Point):
            raise TypeError(f"Input must of type Point, but given {type(p).__name__}")

        if len(self.arr) < self.size:
            self.arr.append(p)
            return True

        mt = self.bbox.midpoint()
        bl = self.bbox.bl 
        tr = self.bbox.tr 

        self.ne = Quadtree(Rectangle(mt, tr), self.size)
        self.sw = Quadtree(Rectangle(bl, mt), self.size) 

        tl: Point = Point(bl.x, tr.y)
        br: Point = Point(tr.x, bl.y)

        self.nw = Quadtree(Rectangle(Point(tl.x, mt.y), Point(mt.x, tl.y)), self.size)
        self.se = Quadtree(Rectangle(Point(br.x, tl.y), Point(tl.x, br.y)), self.size)

        return self.ne.insert(p) or self.nw.insert(p) or self.se.insert(p) or self.sw.insert(p)
    
    

    



            
    


        
