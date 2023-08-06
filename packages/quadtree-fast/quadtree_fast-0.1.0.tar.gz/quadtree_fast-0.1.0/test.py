import quadtree as q
import numpy as np
import time

points = np.random.random((70000, 2))

t0 = time.time()

boundary = q.Rect(0, 0, 360, 180)
qt = q.QuadTree(
    boundary,
    100,
    0
)

for x, y in points:
    x *= 5
    x -= 2.5
    y *= 5
    y -= 2.5
    point = q.Point(x, y)
    qt.insert(point)

len(qt)

query_bound = q.Rect(2, 2, 1, 1)
pts = qt.query_rect(query_bound)
circ_pts = qt.query_radius(2, 2, 0.5)

print(len(pts), len(circ_pts))

print("%.3f seconds" % (time.time() - t0))