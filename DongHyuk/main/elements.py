from abc import ABC, abstractmethod
from json import dump
from os import makedirs
from shutil import rmtree
from shapely.geometry import Polygon, LineString, Point, mapping
from scipy.spatial import Delaunay
import numpy as np
import rhino3dm as rh

def replace_nan_with_str(data_dict):
            for key in data_dict:
                if isinstance(data_dict[key], float) and data_dict[key] != data_dict[key]:
                    data_dict[key] = 'NaN'
                    
def coords_to_rhino_point(coords):
            return rh.Point3d(coords[0],coords[1],0)
                          
class Element(ABC):
    doc_rh = rh.File3dm()
    @abstractmethod
    def build_to_rhino(self):
        pass


class BuildingElement(Element):
    
    FLOOR_HEIGHT = 4.0
    
    def __init__(self, dict_properties: dict):
        
        self.floor = dict_properties["층수"]
        self.name = dict_properties["주기"]
        self.type = dict_properties["종류"]
        self.usage = dict_properties["용도"]
        self.geometry_object = dict_properties["geometry"]
        self.geometry = mapping(dict_properties["geometry"]) #dict
        self.dictionary_prop = dict_properties
        
        replace_nan_with_str(self.dictionary_prop)
        self.dictionary_prop["geometry"] = self.geometry

    def build_to_rhino(self):
        coords = self.geometry['coordinates'][0]
        points = rh.Point3dList([coords_to_rhino_point(coord) for coord in coords])
        
        poly_line = rh.Curve.CreateControlPointCurve(points,1)
        Extrusion = rh.Extrusion().Create(poly_line, -1 * self.floor * self.FLOOR_HEIGHT,True)
        Element.doc_rh.Objects.AddExtrusion(Extrusion)
        
    def __str__(self):
        return f"Building Element Object : Floor : {self.floor} | Name : {self.name} | Type : {self.type} | Usage : {self.usage}"


class VegetationElement(Element):
    def __init__(self, dict_properties: dict):
        self.geometry_object = dict_properties["geometry"]
        self.geometry = mapping(dict_properties["geometry"]) #dict
        self.dictionary_prop = dict_properties
        
        replace_nan_with_str(self.dictionary_prop)
        self.dictionary_prop["geometry"] = self.geometry

    def build_to_rhino(self):
        coord = self.geometry['coordinates']
        point = coords_to_rhino_point(coord)
    
        Element.doc_rh.Objects.AddPoint(point)


class ContourElement(Element):
    
    resolution_of_division = 10
    divided_points = []
    
    def __init__(self, dict_properties: dict):
        self.elevation = dict_properties["등고수치"]
        self.type = dict_properties["구분"]
        self.geometry_object = dict_properties["geometry"]
        
        self.geometry = mapping(dict_properties["geometry"]) #dict
        self.dictionary_prop = dict_properties
        
        replace_nan_with_str(self.dictionary_prop)
        self.dictionary_prop["geometry"] = self.geometry

    def build_to_rhino(self):
        coords = self.geometry['coordinates']
        #move each points to elevation(z-axis)
        points = [rh.Point3d(coord[0],coord[1],self.elevation) for coord in coords]
        curve = rh.Curve.CreateControlPointCurve(points,1)
        Element.doc_rh.Objects.AddCurve(curve)

    @classmethod
    def build_to_surface(cls):
        pts = ContourElement.divided_points
        print(pts)
        rg.Mesh.CreateFromTesslations()
class RoadElement(Element):
    def __init__(self, dict_properties: dict):
        self.geometry_object = dict_properties["geometry"]
        self.geometry = mapping(dict_properties["geometry"]) #dict
        self.dictionary_prop = dict_properties
        
        replace_nan_with_str(self.dictionary_prop)
        self.dictionary_prop["geometry"] = self.geometry

    def build_to_rhino(self):
        coords = self.geometry['coordinates'][0]
        points = [rh.Point3d(coord[0],coord[1],0) for coord in coords]
        curve = rh.Curve.CreateControlPointCurve(points,1)
        
        Element.doc_rh.Objects.AddCurve(curve)
                


