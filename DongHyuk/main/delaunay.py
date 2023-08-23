from itertools import combinations as cb
import ghpythonlib.components as ghcomp
import Rhino.Geometry as geo
tuples = list(cb(x,3))
def is_pt_inside(pt, region):
    plane = geo.Plane.WorldXY
    tol =0.01
    int_result = ghcomp.ClipperComponents.PolylineContainment(
        circle, pt, plane, tol
    )
    if int_result ==1:
        return True
    return False
res = [] 
for tuple in tuples:
    x1,y1 = tuple[0].X, tuple[0].Y
    x2,y2 = tuple[1].X, tuple[1].Y
    x3,y3 = tuple[2].X, tuple[2].Y
    if (x1 -x2) *(y3-y2) - (y1-y2)*(x3-x2) !=0:
        circle = geo.Circle(*tuple)
        delaunay = 0
        if all(not is_pt_inside(pt,circle) for pt in x):
            polyline = geo.PolylineCurve([tuple[0],tuple[1],tuple[2],tuple[0]])
            res.append(polyline)
a= res