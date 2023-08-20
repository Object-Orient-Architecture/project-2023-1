# -*- coding:utf-8 -*-
import Rhino.Geometry as geo
def explode(boundary):
    # 여기를 구현
    print("start drawing tree")
    print(boundary)

    #https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.curve/getlength
    print(boundary.GetLength())

    # https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.polylinecurve/topolyline
    print(boundary.ToPolyline())
    polyline = boundary.ToPolyline()
    lines = [] 
    # https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.polyline
    # Polyline 객체는 Point3d 리스트를 상속받기 때문에 리스트의 속성을 가집니다.
    # 인덱스로 접근하거나 for 문으로 순차적 접근이 가능합니다.
    # 즉 정의상 polyline은 순서가 있는 점의 리스트인 것입니다. 

    # polyline의 인덱스로 접근합니다.
    for i in range(len(polyline)) :
        # i번째 포인트와 i+1번째 포인트에 접근해서 선을 형성합니다.
        point = polyline[i]
        point_next = polyline[(i+1)%len(polyline)]

        # i번째 포인트와 i+1번째 포인트에 접근해서 선을 형성합니다.
        line = geo.LineCurve(point, point_next)
        lines.append(line)

    return lines