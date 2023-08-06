class Point(object):
    """
    2D point with optional data attachment.
    """
    x: float
    y: float

    def __init__(self, x: float, y: float, data: any = None) -> Point: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def distance_to(self, other: Point) -> float:
        """
        Calculates the distance to another Point.
        """

class Rect(object):
    """
    Rectangle.
    """

    def __init__(self, center_x: float, center_y: float, width: float, height: float) -> Rect:
        """
        Creates a new rectangle given the center x and y coordinates and the width and height to expand outwards.
        """
    
    def contains(self, point: Point) -> bool:
        """
        Returns whether the point is inside of the rectangle.
        """
    
    def intersects(self, rect: Rect) -> bool:
        """
        Returns whether the rectangle intersects another rectangle.
        """

class QuadTree(object):
    """
    Quadtree for spatial indexing based on https://scipython.com/blog/quadtrees-2-implementation-in-python/.
    """

    def __init__(self, boundary: Rect, max_points: int, depth: int) -> QuadTree:
        """
        Creates a new quadtree with the specified boundary and maximum number of points in the node.
        """
    
    def insert(self, point: Point) -> bool:
        """
        Attempts to insert the point in the quadtree or a subtree and returns if successful or not.
        """
    
    def query_rect(self, boundary: Rect) -> list[Point]:
        """
        Finds and returns all points within the specified rectangular boundary.
        """
    
    def query_radius(self, center_x: float, center_y: float, radius: float) -> list[Point]:
        """
        Finds and returns all points within the specified circular boundary.
        """
    
    def __len__(self) -> int:
        """
        Returns the number of points in the quadtree.
        """