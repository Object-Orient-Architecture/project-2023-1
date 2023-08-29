import rhinoscriptsyntax as rs

class RhinoProcessor:
  '''
  Rhino Python APIs like "rhinoscriptsyntax" are only able to running in the Rhinoceros Software
  This class is for running the only-in-rhino scripts that provides familiar functions like project,   move, curveboolean and so on.
  '''
  
  # 1 . Properties
  def __init__(self):
    '''
    Get object variable to control them by layer that the SMA application already distinguished
    '''
    def __select_object_by_layer():
      return rs.ObjectsByLayer(layer)
  
    self.contour_mesh = __select_object_by_layer("Contour")
    self.road_crvs = __select_object_by_layer("Road")
    ... #same for other elements like vegetation_pts, and building_breps
    
    #Additionally, convert the Geometry type to a type easy to use
    self.contour_srf = rs.MeshToNURB(self.contour_mesh)
    
  # 2 . Get Contour Polysurface following the provided option
  def process_contour(option:ContourType):
    '''
    From the mesh and te options the application provided, to result of contour surface
    the purpose is to get "self.contour_polysrf" which is the result meeting options
    '''
    def __drape_and_contour(contour): #type : original surface -> contoured curves
      #...implementation
      return contour_crv
    
    def __solidize_surface(contour_srf): #type : origin surface -> polysurfaces having volume
      #...implementation
      return contour_polysrf
      
    def __extrude_contour(contour_crv): #type : contour curves -> extruded polysurfaces or extrusions
      #...implementation : code below is not real implementation but conceptualized psuedo code
      for crv in contour_crv: extrude(options.contour_height)
      return contour_polysrf
      
    if option == ContourType.Surface : self.contour_polysrf = __solidize_surface(self.contour_srf)
  elif option == ContourType.Contour : 
    self.contour_crv  	 = __drape_and_contour(self.contour_srf)
    self.contour_polysrf = __extrude_contour(self.contour_crv)
    
  # 3 . Project other elements to the contour polysurface
  # 3 - 1 . for building elements
  def project_building():
    '''
    method __project()
    1. get building extrusion's base curve
    2. projects base curves' vertices onto contour polysurface
    3. find the most shortest projection of the points
    4. move building brep in Z-axis way, and the distance is the value I get from the process 3
    '''
    for building in self.building_breps:
    	#...implementation : code below is not real implementation but conceptualized psuedo code
		__project(building,self.contour_polysrf)
        
        
  # 3 - 2 . for vegetation elements     
  def project_vegetation():
    Z_AXIS = (0,0,1)
    self.vegetation_pts = rs.ProjectPointToMesh(self.vegetation_pts,
                                                self.contour_polysrf,
                                                Z_AXIS)
  # 3 - 3 . for road elements
  def project_road():
    '''
    method __project()
    1. divide case : one for contour, one for surface
   	if contourType = surface:
    	2. curveBooleanUnion the road_crvs
        3. project the curve onto surface
        4. copy the contour surface and split with the curve
        5. Offset the surface with thickness 2
    elif contourType = Contour:
    	2. curveBooleanUnion the road_crvs
        3. split the curve with the contour_crvs
        4. Make the splitted curve planar surface
        5. project the surfaces onto the contour
        6. Thicken the projected with thickness 2
    '''
    __project(self.road_crvs, self.contour_polysrf)
    
processor = RhinoProcessor()
processor.process_contour(options)
processor.project_building()
processor.project_vegetation()
processor.project_r