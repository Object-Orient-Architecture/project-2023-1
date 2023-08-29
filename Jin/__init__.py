import ezdxf
import random
from matplotlib.path import Path


def get_bounding_box(polyline):
    vertices = polyline.vertices
    xs = [vertex.dxf.location.x for vertex in vertices]
    ys = [vertex.dxf.location.y for vertex in vertices]
    return min(xs), min(ys), max(xs), max(ys)


def random_points_within_polygon(poly, num_points):
    points = []
    minx, miny, maxx, maxy = get_bounding_box(poly)

    # Convert the Polyline vertices to a Path for point containment check
    path_coords = [(v.dxf.location.x, v.dxf.location.y) for v in poly.vertices]
    path = Path(path_coords)

    while len(points) < num_points:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        if path.contains_point((x, y)):
            points.append((x, y))
    return points


# 1. 조경 영역만 닫힌 폴리라인으로 표시된 입력한 DWG 파일 읽기
file_path = input("DWG 파일 경로 입력: ")
doc = ezdxf.readfile(file_path)
msp = doc.modelspace()

# 2. 2D이며 닫힌 POLYLINE을 찾아 나무 심는 점을 랜덤하게 생성
closed_2d_polylines = [
    entity
    for entity in msp.query("POLYLINE")
    if entity.is_closed and entity.is_2d_polyline
]
if not closed_2d_polylines:
    print("조경 영역 없음")
    exit()

polyline = closed_2d_polylines[0]
num_points = int(input("나무 몇개 심을깝쇼?: "))
points = random_points_within_polygon(polyline, num_points)

# 3. 점을 중심으로 나무 반경원을 그리기
for point in points:
    msp.add_circle(center=point, radius=1000)  # 지름이 2m이므로 반지름은 1m입니다.

# 조경그려진 DWG 저장
output_path = input("파일 어디다 저장할깝쇼?: ")
doc.saveas(output_path)
print("조경 완!")
