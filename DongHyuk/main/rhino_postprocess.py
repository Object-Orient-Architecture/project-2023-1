import rhinoscriptsyntax as rs

#Select Object -> Guid
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

#Get Objects of the file
contour_mesh = select_obj_by_type("Mesh")
vegetation_pts = select_obj_by_type("Point")
road_crvs = select_obj_by_type("Curve")

#Vegetation Projection
projected_vegetation = rs.ProjectPointToMesh(vegetation_pts,contour_mesh,(0,0,1))

#Add to File + remove Origin
rs.AddPoints(projected_vegetation)
rs.DeleteObjects(vegetation_pts)

#Planar Road Curves
group_road = rs.AddGroup("Road")
rs.AddObjectsToGroup(road_crvs,group_road)

road_srf = rs.AddPlanarSrf(rs.ObjectsByGroup(group_road))
rs.DeleteObjects(road_crvs)


