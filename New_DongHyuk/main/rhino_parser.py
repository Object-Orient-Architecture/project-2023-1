import rhino3dm
from shapely.geometry import Polygon
from shapely.ops import transform
from functools import partial

# Shapely 다각형 생성 (예시)
shapely_polygon = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])

# Shapely 좌표를 Rhino 좌표로 변환하는 함수
def shapely_to_rhino_coord(x, y, z):
    return rhino3dm.Point3d(x, y, z)

# Shapely 좌표를 Rhino 좌표로 변환하여 CurvePoint 배열 생성
rhino_points = [shapely_to_rhino_coord(x, y, 0) for x, y in shapely_polygon.exterior.coords]

# Rhino 좌표를 Shapely 좌표로 변환하는 함수
def rhino_to_shapely_coord(point):
    return (point.X, point.Y)

# Shapely 좌표계와 Rhino 좌표계 간 변환 함수
def transform_to_shapely_coords(rhino_point):
    shapely_point = transform(partial(rhino_to_shapely_coord), rhino_point)
    return shapely_point

# CurvePoint 배열로부터 Rhino Curve 생성
rhino_curve = rhino3dm.Curve.CreateInterpolatedCurve(rhino_points, 3)

# Rhino Curve를 Shapely 다각형으로 변환
shapely_polygon_converted = transform(transform_to_shapely_coords, rhino_curve)

print("Shapely 다각형:")
print(shapely_polygon)
print("변환된 Rhino Curve:")
print(rhino_curve)
print("변환된 Shapely 다각형:")
print(shapely_polygon_converted)
