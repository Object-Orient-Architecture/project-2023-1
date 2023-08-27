from abc import ABC, abstractmethod

####IT IS FOR DEBUGGING####
from json import dump
from os import makedirs
from shutil import rmtree
from shapely.geometry import Polygon, LineString, Point, mapping
import bbox_check as bb 
import rhino3dm as rh

class Model:
    def __init__(self):
        self.file_dir = 'C:/Users/ERSATZ-CAMPUSTOWN/Documents/GitHub/project-2023-1/Junmin/rhino_md/rhino_temp.3dm'
        self.file3dm = rh.File3dm()
    def build_to_rhino(self):
        bool = self.file3dm.Write(self.file_dir, 7)
        return bool
        


def coords_to_rhino_point(coords):
    return rh.Point3d(coords[0],coords[1],0)

class InterestPostProcess: 
    def __init__(self, model: Model,  interest_list:list):
        self.interest_list = interest_list
        self.model = model
    
    def build_to_rhino(self, heightdict, heightscale):
        for interest in self.interest_list:
            for polygon in interest.polygons:

                height = heightdict[interest.name]*heightscale


                coords = polygon.exterior.coords


                points = rh.Point3dList([coords_to_rhino_point(coord) for coord in coords])

                poly_line = rh.Curve.CreateControlPointCurve(points,1)

                Extrusion_up = rh.Extrusion().Create(planarCurve = poly_line, height =  float(height), cap = True)
                Extrusion_down = rh.Extrusion().Create(planarCurve = poly_line,height = - float(height), cap = True)
                
                if (Extrusion_up is not None):
                    
                    bbox = Extrusion_up.GetBoundingBox()

                    bool = bbox.Center.Z > 0
                    if bool:
                        self.model.file3dm.Objects.AddExtrusion(Extrusion_up)
                    else:
                        self.model.file3dm.Objects.AddExtrusion(Extrusion_down)


        
                          
class BuildingPostProcess: 
    def __init__(self, model: Model, building_dict:dict):
        self.building_dict = building_dict
        self.model = model
    
    def build_to_rhino(self, heightscale:int, heightdict:dict ):
        def draw_coord_to_extrusion(polygon, height):
            coords = polygon.exterior.coords

            points = rh.Point3dList([coords_to_rhino_point(coord) for coord in coords])

            poly_line = rh.Curve.CreateControlPointCurve(points,1)

            # poly_line.ClosedCurveOrientation
            

            Extrusion_up = rh.Extrusion().Create(planarCurve = poly_line, height =  float(height), cap = True)
            Extrusion_down = rh.Extrusion().Create(planarCurve = poly_line,height = - float(height), cap = True)
            
            if (Extrusion_up is not None):
                
                bbox = Extrusion_up.GetBoundingBox()

                bool = bbox.Center.Z > 0
                if bool:
                    self.model.file3dm.Objects.AddExtrusion(Extrusion_up)
                else:
                    self.model.file3dm.Objects.AddExtrusion(Extrusion_down)


        for name, buildings in self.building_dict.items():
            height = heightdict[name] * heightscale
            for building in buildings:
                polygon = building.polygon

                new_height= height * building.floor


                if polygon.geom_type == 'MultiPolygon':
                    for geom in polygon.geoms:
                        draw_coord_to_extrusion(geom, new_height)
                elif polygon.geom_type == 'Polygon':
                    draw_coord_to_extrusion(polygon, new_height)





                else:
                    pass





                
                
        #         success = self.model.build_to_rhino()
        #         print (success)
        


# class BuildingElement(Element):
    
#     # FLOOR_HEIGHT = 4.0
    
#     # def __init__(self, dict_properties: dict):
        
#     #     self.floor = dict_properties["층수"]
#     #     self.name = dict_properties["주기"]
#     #     self.type = dict_properties["종류"]
#     #     self.usage = dict_properties["용도"]
#     #     self.geometry_object = dict_properties["geometry"]
#     #     self.geometry = mapping(dict_properties["geometry"]) #dict
#     #     self.dictionary_prop = dict_properties
        
#     #     replace_nan_with_str(self.dictionary_prop)
#     #     self.dictionary_prop["geometry"] = self.geometry

#     def build_to_rhino(self):
        
        
#         coords = self.geometry['coordinates'][0]
#         points = rh.Point3dList([coords_to_rhino_point(coord) for coord in coords])
        
#         poly_line = rh.Curve.CreateControlPointCurve(points,1)
#         Extrusion = rh.Extrusion().Create(poly_line, -1 * self.floor * self.FLOOR_HEIGHT,True)
#         Element.doc_rh.Objects.AddExtrusion(Extrusion)
        
        
    
    # def __str__(self):
    #     return f"Building Element Object : Floor : {self.floor} | Name : {self.name} | Type : {self.type} | Usage : {self.usage}"


# class VegetationElement(Element):
#     def __init__(self, dict_properties: dict):
#         self.geometry_object = dict_properties["geometry"]
#         self.geometry = mapping(dict_properties["geometry"]) #dict
#         self.dictionary_prop = dict_properties
        
#         replace_nan_with_str(self.dictionary_prop)
#         self.dictionary_prop["geometry"] = self.geometry

#     def build_to_rhino(self):
#         coord = self.geometry['coordinates']
#         point = coords_to_rhino_point(coord)
    
#         Element.doc_rh.Objects.AddPoint(point)


# class ContourElement(Element):
    
#     resolution_of_division = 10
#     divided_points = []
    
#     def __init__(self, dict_properties: dict):
#         self.elevation = dict_properties["등고수치"]
#         self.type = dict_properties["구분"]
#         self.geometry_object = dict_properties["geometry"]
        
#         self.geometry = mapping(dict_properties["geometry"]) #dict
#         self.dictionary_prop = dict_properties
        
#         replace_nan_with_str(self.dictionary_prop)
#         self.dictionary_prop["geometry"] = self.geometry

#     def build_to_rhino(self):
#         coords = self.geometry['coordinates']
#         #move each points to elevation(z-axis)
#         points = [rh.Point3d(coord[0],coord[1],self.elevation) for coord in coords]
#         curve = rh.Curve.CreateControlPointCurve(points,1)
#         ContourElement.divided_points.append(rcc.DivideByCount1(curve,ContourElement.resolution_of_division,True))
#         Element.doc_rh.Objects.AddCurve(curve)


#     def build_to_surface():
#         pts = ContourElement.divided_points
#         print(pts)
    
# class RoadElement(Element):
#     def __init__(self, dict_properties: dict):
#         self.geometry_object = dict_properties["geometry"]
#         self.geometry = mapping(dict_properties["geometry"]) #dict
#         self.dictionary_prop = dict_properties
        
#         replace_nan_with_str(self.dictionary_prop)
#         self.dictionary_prop["geometry"] = self.geometry

#     def build_to_rhino(self):
#         pass