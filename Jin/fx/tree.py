# -*- coding:utf-8 -*-

import random
import math
import Rhino.Geometry as geo  # type: ignore


def get_bounding_box(polyline):
    vertices = polyline.vertices
    xs = [vertex.dxf.location.x for vertex in vertices]
    ys = [vertex.dxf.location.y for vertex in vertices]
    return min(xs), min(ys), max(xs), max(ys)


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_random_points(tree_radius, num_points, boundary):
    points = []
    # minx, miny, maxx, maxy = (0, 0, 4000, 4000)
    bbox = boundary.GetBoundingBox(geo.Plane.WorldXY)
    box = geo.Box(geo.Plane.WorldXY, bbox)
    x_interval, y_interval = box.X, box.Y
    minx, maxx = x_interval.Min, x_interval.Max
    miny, maxy = y_interval.Min, y_interval.Max

    for _ in range(num_points):
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        pt = geo.Point3d(x, y, 0)
        points.append(pt)

    return points


def main(tree_radius, num_points, boundary):
    ##tree_radius = float(input("나무 반경 얼마입니까? (mm): "))
    ##num_points = int(input("나무 몇개 심을깝쇼?: "))
    points = get_random_points(tree_radius, num_points, boundary)
    circles = []
    for point in points:
        circle = geo.Circle(point, tree_radius)
        curve = circle.ToNurbsCurve()
        circles.append(curve)
    return circles
    output_path = input("파일 어디다 저장할깝쇼?: ")
    doc.saveas(output_path)
    print("조경 완료!")


# box = geo.Box(geo.Plane, polyline)
# x_interval, y_interval = box.X, box.Y
# minx, maxx = x_interval.Min, x_interval.Max
# miny, maxy = y_interval.Min, y_interval.Max
