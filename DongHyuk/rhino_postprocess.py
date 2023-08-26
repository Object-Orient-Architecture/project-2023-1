import rhinoscriptsyntax as rs

def select_obj_by_type(type):
    rs.UnselectAllObjects()
    if type == "Mesh":
        rs.Command("_SelMesh",echo=False)
    if type == "Point":
        rs.Command("_SelPt",echo=False)
    if type == "Curve":
        rs.Command("_SelCrv",echo=False)       
        
    obj = rs.SelectedObjects()
    rs.UnselectAllObjects()
    return obj

contour_mesh = select_obj_by_type("Mesh")
vegetation_pts = select_obj_by_type("Point")
road_crvs = select_obj_by_type("Curve")
projected_vegetation = rs.ProjectPointToMesh(vegetation_pts,contour_mesh,(0,0,1))

rs.AddPoints(projected_vegetation)
rs.DeleteObjects(vegetation_pts)

