from abc import ABC, abstractmethod
from json import dump
from os import makedirs
from shutil import rmtree
from shapely.geometry import Polygon, LineString, Point, mapping
from scipy.spatial import Delaunay
from itertools import permutations, combinations
import numpy as np
import rhino3dm as rh
from copy import deepcopy

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
    curves = []
    
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
        ContourElement.curves.append(curve)
        # Element.doc_rh.Objects.AddCurve(curve)

    @classmethod
    def build_to_surface(cls):
        #Group by Elevation
        def __group_to_connect(data_list,elev_list):
            grouped_data = {}
            for data, elev in zip(data_list, elev_list):
                if data.IsClosed:
                    continue
                elif elev in grouped_data:
                    grouped_data[elev].append(data)
                else:
                    grouped_data[elev] = [data]
            return grouped_data
        
        elev_grouped_curves = __group_to_connect(ContourElement.curves,[curve.PointAtEnd.Z for curve in ContourElement.curves])
    
        #Connect curves with same elevation
        def connected_len(curves):
            length = 0
            for i in range(len(curves)):
                if i == len(curves)-1:
                    bet_len = 0
                else:
                    bet_len = curves[i].PointAtEnd.DistanceTo(curves[i+1].PointAtStart)
                length += bet_len
                    
                if(isinstance(curves[i],rh.LineCurve)):
                    length += curves[i].Line.Length
                else:
                    length += curves[i].ToPolyline().Length
                    
            return length
        
        #find shortest connected curves
        def connect_curves(curves):
            joined_curve = rh.PolyCurve()
            joined_curve.Append(curves[0])
            for curve in curves[1:]:
                joined_curve.Append(curve)
            return joined_curve
        
        def redirect_curves(curves:list):
            pass
            
                        
                        
            
            
        rep_elev_curve = {}
        for elev,curve_group in elev_grouped_curves.items():
            if len(curve_group) == 1:
                rep_elev_curve[elev] = curve_group[0]
                print(f'elevation = {elev}')
                print(f'curve_group = {curve_group}')
                print("-------------------")
                print("One Curve")
                print("-------------------")
                print()
                
            else:
                print(f'elevation = {elev}')
                print(f'curve_group = {curve_group}')
                print("-------------------")
                                
                i = 0
                min_i = 0
                min_len = 0
                
                perms = list(permutations(curve_group,len(curve_group)))
                print(f'perms len  = {len(list(perms))}')
                print(f'min_i = {min_i}')
                
                for perm in list(perms):
                    perm = list(perm)
                    if min_len == 0:
                        min_len = connected_len(perm)
                        min_i = i
                    elif min_len >= connected_len(perm):
                        min_len = connected_len(perm)
                        min_i = i
                        
                    if i != len(list(perms))-1:
                        i+=1
                    else:

                        rep_elev_curve[elev] = connect_curves(perms[min_i])
                    
                print(f'perms len  = {len(list(perms))}')
                print(f'min_i = {min_i}')
                print("-------------------")
                print()
                    
        for curve in rep_elev_curve.values():

            print(curve)
            Element.doc_rh.Objects.AddCurve(curve)
                 
            
        #divide curves
        for curve in ContourElement.curves:
            # print(curve.PointAtEnd.Z)
            pass
        
        
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
                


