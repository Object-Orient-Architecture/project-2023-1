# import numpy as np
# from scipy.spatial import Delaunay
# import rhino3dm as rh

# def get_points_to_array(points:list):
#         return np.array(points)

# triangles = Delaunay(get_points_to_array([[0, 0], [0, 1.1], [1, 0], [1, 1]]))
# print(triangles.simplices)

import rhinoinside as ri
import sys

ri.load()