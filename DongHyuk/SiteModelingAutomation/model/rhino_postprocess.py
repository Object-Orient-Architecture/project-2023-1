import rhinoscriptsyntax as rs
import Rhino.Geometry as geo

def set_camera_view():
    view_name = "Perspective" 
    camera_location = (10, 10, 10)  
    camera_target = (0, 0, 0)  
    camera_up_vector = (0, 0, 1)  
    camera_scale = 1 

    rs.ViewCamera(view_name, [camera_location, camera_target, camera_up_vector])


def main():
    print("MAIN CALLED")
    set_camera_view()
    #CONST
    Z_AXIS = (0,0,1)
    #Select Object by Layer
    def sel_obj_by_layer(layer):
        return rs.ObjectsByLayer(layer)
    
    contour_mesh = sel_obj_by_layer('Contour')
    road_crv = sel_obj_by_layer('Road')
    vegetation_pts = sel_obj_by_layer('Vegetation')
    building_obj = sel_obj_by_layer('Building')
    
    #Project vegetation onto contour mesh
    projected_vegetation_pts = rs.ProjectPointToMesh(vegetation_pts,contour_mesh,(0,0,1))
    rs.CurrentLayer("Vegetation")
    rs.AddPoints(projected_vegetation_pts)
    rs.DeleteObjects(vegetation_pts)
    
    #Mesh to NURB
    print(contour_mesh)
    contour_srf = rs.MeshToNurb(contour_mesh,delete_input=True)
    
    #Project Building
    def building_to_srf(building,srf):
        z_axis = (0,0,1)
        #Get Vertices
        vertices = rs.SurfacePoints(building)
        #Cull dups
        culled = rs.CullDuplicatePoints(vertices)
        #Cull Higher
        base_pts = []
        for pt in culled:
            if pt.Z == 0:
                base_pts.append(pt)
        #Project to Srf
        results = rs.ProjectPointToSurface(base_pts,srf,(0,0,1))
        #Find Lowest
        i = 0
        min_i = 0
        min_len = 0
        for pt in results:
            if min_len == 0 or min_len > pt.Z:
                min_i = i
                min_len = pt.Z
            else:
                continue
            i += 1
        print(results)
        lowest_pt = results[min_i]
        lowest_pt_correspond = base_pts[min_i]
        target_z = lowest_pt.Z
        origin_z = lowest_pt_correspond.Z
        
        #move Building
        return (0,0,target_z - origin_z)
        
    for building in building_obj:
        move_vect = building_to_srf(building,contour_srf)
        rs.MoveObjects(building,move_vect)
    
    #Road to Surface
    rs.CurrentLayer("Road")
    road_union_crv = rs.CurveBooleanUnion(road_crv)
    rs.DeleteObjects(road_crv)
    
    road_mapped = rs.ProjectCurveToSurface(road_union_crv,contour_srf,Z_AXIS)
    rs.DeleteObjects(road_union_crv)
    
    # #Contour
    # rs.HideObjects(rs.ObjectsByLayer("Building"))
    # bbox = rs.BoundingBox(contour_srf)
    # min_h, max_h = list(set([pt.Z for pt in bbox]))
    # lower_crv = [pt for pt in bbox if pt.Z == min_h]
    # lower_crv.append(lower_crv[0])
    # base_line = rs.AddPolyline(lower_crv)
    
    # base_line = rs.OffsetCurve(base_line,(0,0,0),20)
    # knots = rs.CurvePoints(base_line)
    # drape_start = "{},{},{}".format(knots[0].X,knots[0].Y,knots[0].Z)
    # drape_end = "{},{},{}".format(knots[2].X,knots[2].Y,knots[2].Z)
    # rs.Command("OneView")
    # rs.CurrentView("Top")
    # rs.AddLayer("Drape")
    # rs.CurrentLayer("Drape")
    # rs.Command("_SelAll _Zoom S")
    # rs.Command("Drape Spacing 1 {0} {1}".format(drape_start,drape_end))
    # rs.CurrentView("Perspective")
    # drape = rs.ObjectsByLayer("Drape")
    # rs.ObjectName(drape,"DRAPE")
    # rs.HideObject(contour_srf)
    # rs.SelectObject(rs.ObjectsByName("drape"))
    # rs.Command("Contour 0,0,1 0,0,2 5")
    # rs.HideObject(drape)
    # contour_crv = rs.ObjectsByLayer("Drape")
    
    # for crv in contour_crv:
    #     try:
            
    #         if not rs.IsCurveClosed(crv) and rs.IsCurveClosable(crv):
    #             rs.UnselectAllObjects()
    #             rs.SelectObject(crv)
    #             rs.Command("CloseCurve")
                
    #         rs.UnselectAllObjects()
    #         rs.SelectObject(crv)           
    #         rs.Command("Extrude 5")
    #     except Exception as e:
    #         print(e)

    # rs.ShowObjects(rs.ObjectsByLayer("Building"))
if __name__ == "__main__":
    main()
