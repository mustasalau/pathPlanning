#  Code is used for collision checking. It defines an Axis-Aligned Bounding Box (AABB) class for 3D point clouds.
class AABB:
    def __init__(self, min_point, max_point):
        self.min = min_point
        self.max = max_point

    @classmethod
    # Identifies the minimum and maximum corners of the bounding box from a set of 3D points.
    def from_points(cls, points):
        min_p = [float('inf'), float('inf'), float('inf')]
        max_p = [float('-inf'), float('-inf'), float('-inf')]
        for p in points:
            min_p = [min(min_p[i], p[i]) for i in range(3)] # component-wise min
            max_p = [max(max_p[i], p[i]) for i in range(3)] # component-wise max
        return cls(min_p, max_p)
    
    def point_inside(self, point):
        return all(self.min[i] <= point[i] <= self.max[i] for i in range(3))

    def boxes_intersect(self, other):
        for i in range(3):
            if self.max[i] < other.min[i] or self.min[i] > other.max[i]:
                return False
        return True

cloud_data = [
    [1.0,  5.0,  2.0],
    [-2.0, 3.0,  0.0],
    [4.0, -1.0,  1.0],
    [0.0,  0.0,  9.0]
]
my_box = AABB.from_points(cloud_data)
print("Box Min Corner:", my_box.min)
print("Box Max Corner:", my_box.max)
print("Is Point [0.0, 0.0, 0.0] inside box:", my_box.point_inside([0.0, 0.0, 0.0]))