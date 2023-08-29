# -*- coding:utf-8 -*-
import Rhino.Geometry as geo
import random
import math
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghcomp
import scriptcontext as sc


# from typing import List
def check_contain(pt, boundary):
    # type: (geo.Curve, geo.Point3d) -> bool
    # -1: 일치, 0: 밖, 1: 안
    int_result = ghcomp.ClipperComponents.PolylineContainment(
        boundary, pt, geo.Plane.WorldXY, 0.1
    )
    return int_result == 1


# 바운더리 커브 안에 랜덤 시드 생성
def get_random_point_in_curve_boundary(boundary_curve):
    bbox = boundary_curve.GetBoundingBox(True)
    pts = []
    for _ in range(100):
        x = random.uniform(bbox.Min.X, bbox.Max.X)
        y = random.uniform(bbox.Min.Y, bbox.Max.Y)
        pt = geo.Point3d(x, y, 0)
        pts.append(pt)
        if check_contain(pt, boundary_curve):
            sc.sticky["pts"] = pts
            return pt
        ##rs 안쓰고 포인트 포함관계 확인 코드로 수정


# Import Grasshopper using the .NET Common Language Runtime AddReference function
import clr

clr.AddReference("Grasshopper")
import Grasshopper as gh


def voronoi2D(nodePts, boundary):
    # type: (List[geo.Point], geo.Curve) -> List[geo.Curve]
    # Create a boundingbox and get its corners
    bbox = boundary.GetBoundingBox(True)
    diagnoal_line = bbox.Diagonal
    diagnoal_line_length = diagnoal_line.Length
    # f = diagnoal_line_length / 15
    # bbox.Inflate(f, f, f)
    bboxCorners = bbox.GetCorners()

    # Create a list of nodes
    nodes = gh.Kernel.Geometry.Node2List()
    for p in nodePts:
        n = gh.Kernel.Geometry.Node2(p.X, p.Y)
        nodes.Append(n)

    # Create a list of outline nodes using the BB
    outline = gh.Kernel.Geometry.Node2List()
    for p in bboxCorners:
        n = gh.Kernel.Geometry.Node2(p.X, p.Y)
        outline.Append(n)

    # Calculate the delaunay triangulation
    delaunay = gh.Kernel.Geometry.Delaunay.Solver.Solve_Connectivity(nodes, 0.1, False)

    # Calculate the voronoi diagram
    voronoi = gh.Kernel.Geometry.Voronoi.Solver.Solve_Connectivity(
        nodes, delaunay, outline
    )

    # Get polylines from the voronoi cells and return them to GH
    polylines = []
    for c in voronoi:
        pl = c.ToPolyline()
        plc = pl.ToPolylineCurve()
        polylines.append(plc)

    return polylines


# 보로노이 선 오프셋 -> 길 만들기
def offset_voronoi_edges(voronoi_curves, offset_value):
    streets = []
    for curve in voronoi_curves:
        offset_curve = curve.Offset(
            geo.Plane.WorldXY, offset_value, 10, geo.CurveOffsetCornerStyle.Sharp
        )
        if offset_curve:
            streets.extend(offset_curve)
        offset_curve = curve.Offset(
            geo.Plane.WorldXY, -offset_value, 10, geo.CurveOffsetCornerStyle.Sharp
        )
        if offset_curve:
            streets.extend(offset_curve)
    return streets


# 새로만든 지역 안에 씨드 랜덤하게 뿌리기
def random_points_in_region(region_curve, num_points):
    return [get_random_point_in_curve_boundary(region_curve) for _ in range(num_points)]


def get_close_points(pt, tree_points, dist):
    return [
        tree_point for tree_point in tree_points if pt.DistanceTo(tree_point) < dist
    ]


def main(seed_count, boundary_curve):
    seed_points = [
        get_random_point_in_curve_boundary(boundary_curve) for _ in range(seed_count)
    ]
    sc.sticky["seed_points"] = seed_points
    voronoi_curves = voronoi2D(seed_points, boundary_curve)
    street_curves = offset_voronoi_edges(voronoi_curves, 1000)

    voronoi_offset = []
    for curve in voronoi_curves:
        offset_curve = curve.Offset(
            geo.Plane.WorldXY, -1000, 10, geo.CurveOffsetCornerStyle.Sharp
        )
        if offset_curve:
            voronoi_offset.extend(offset_curve)

    # for street in street_regions:
    #     voronoi_regions = [area.Split(street, 1e-4) for area in voronoi_regions]
    #     voronoi_regions = [item for sublist in voronoi_regions for item in sublist]

    tree_points = []
    for region in voronoi_offset:
        region_area = geo.Brep.CreatePlanarBreps(region, 0.1)[0].GetArea()
        num_trees = int(region_area / (math.pi * (1500**2)))
        tree_points += random_points_in_region(region, num_trees)
    checked_points = []

    while tree_points:
        pt = tree_points.pop()
        close_points = get_close_points(pt, tree_points, 1500)
        for close_point in close_points:
            tree_points.remove(close_point)
        checked_points.append(pt)

    return (
        voronoi_curves,
        street_curves,
        checked_points,
        voronoi_offset,
    )


# 직경 1000~2000 사이의 나무 그리기
def draw_trees(tree_points):
    circles = []
    for point in tree_points:
        radius = int(random.uniform(1000, 2000))
        circle = geo.Circle(point, radius)
        circles.append(circle.ToNurbsCurve())
    return circles
