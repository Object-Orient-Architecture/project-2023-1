# -*- coding:utf-8 -*-
import rhino3dm as rs
def explode(boundary):
    # 여기를 구현
    polyline = boundary.ToPolyline()
    lines = [] 
    # polyline의 인덱스로 접근합니다.
    for i in range(len(polyline)-1) :
        # i번째 포인트와 i+1번째 포인트에 접근해서 선을 형성합니다.
        point = polyline[i]
        point_next = polyline[(i+1)]

        # i번째 포인트와 i+1번째 포인트에 접근해서 선을 형성합니다.
        line = rs.LineCurve(point, point_next)
        lines.append(line)

    return lines