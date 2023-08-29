from abc import ABC, abstractmethod
from json import mapping

def create_layer(layer_name, layer_color):
  '''
  create a layer with parameter:name and color
  return layer_attribute which is used when Setting object's layer
  '''
  layer = rhino3dm.Layer()
  layer.Name = layer_name
  layer.Color = layer_color
  layer_index = Element.rhino_document.Layers.Add(layer)
  
  layer_attribute = rhino3dm.ObjectAttributes()
  layer_attribute.LayerIndex = layer_index
  
  return layer_attribute

class Element(ABC):
  '''
  Abstract Super Class - Represent all element class
  All element class should have 'build_to_rhino()' method
  and Each element class should have different properties
  '''
  rhino_document = rhino3dm.File3dm() # class Properties : All element class can reference the documen
  
  @abstractmethod
  def build_to_rhino(self):
    pass
  
class BuildingElement(Element):
  '''
  BuildingElement inherits Elements class so that it should have build_to_rhino() method
  constants : floor_height, building_layer
  Properties : floor, height, base_geometry<List<Point>>
  '''
  
  FLOOR_HEIGHT = 4.0 # Class Properties : Constant
  BUILDING_LAYER = rhino3dm.Layer()
  BUILDING_LAYER.Name = "Building"
  
  def __init__(self,information_json):
    '''
    From shp, read json, and convert it into properties
    '''
    self.floor = information_json["층수"] #type:int
    self.height = FLOOR_HEIGHT * self.floor #type:float
	self.geometry = mapping(information_json["geometry"]) #type:dict (mapping: parse json data to dict)
    
  def build_to_rhino(self):
    '''
    1. Get coordinates<rhino3dm.Point3d> of base curve
    2. Get Polyline<rhino3dm.Curve> with coordinates - with CreateControlPointCurve(points,1). 1 is the		  dimension of the control point
    3. Extrude the curve
    4. add the curve to the Element.rhino_document, and layer it with a name "Building"
    '''
    #implementation
  
class VegetationElement(Element):
  '''	
  VegetationElement inherits Elements class so that it should have build_to_rhino() method
  Properties : base_geometry<Point2d>
  '''
  
  def __init__(self,information_json):
    self.geometry = mapping(information_json["geometry"]) #type:dict
  
  def build_to_rhino(self):
    '''
    1. Get coordinate<rhino3dm.Point2d> of point and add a Z - value 0 
    2. add the point to the Element.rhino_document, and layer it with a name "Vegetation"
    '''
	coord = self.geometry['coordinates']
    point = rhino3dm.Point3d(coord[0],coord[1],0)
    
    # Add Point into Layer "Vegetation" with color Blue
    Element.rhino_document.Objects.Add(point,create_layer("Vegetation",(0,0,255,255)))

class ContourElement(Element):
  '''	
  ContourElement inherits Elements class so that it should have build_to_rhino() method
  Constants : resolution_of_division,contour_curves
  Properties : elevation, base_geometry<List<Point2d>>
  
  Class Properties : contour_curves
  Class Methods : build_to_surface(cls) - make a united surface using scipy.spatial.Delaunay
  '''	    
    #Clas Properties
  resolution_of_division = 10
  contour_curves = []
    
  def __init__(self, information_json):
    self.elevation = information_json["등고수치"] #type:float
    self.geometry = mapping(information_json["geometry"]) #type:dict 
  
  def build_to_rhino(self):
	'''
    This method has almost same with the building's methods but it additionally saves the curve in 		class Property : contour_curves to make a contour_surface in the class method build_to_surface()
    '''
    
  @classmethod        
  def build_to_surface(cls):
    '''
    Procedure
    1. divide all contour curves with approximate length and get points list
    2. Get a vertices of modeling border curve, move it to the height where the Z value is same with 		closest points of the process 1, and add it also to the points list
    2. Make a copy of XY-Plane-Projected points
    3. Using scipy.spatial.Delaunay, make a connection indices of mesh
    4. Create a rhino3dm.Mesh whose vertices are points of process 1 and face indices are that of 		   process 3
    '''
    #...implementation above
    Element.rhino_document.Objects.Add(contour_mesh,create_layer("Contour",(255,0,0,255)))
    
class RoadElement(Element):
  '''
  Same with Building Element but it doesn't extrude the base curve in the method "build_to_rhino()"
  '''

class BorderElement(Element):
  '''
  Same with RoadElement
  '''