from abc import ABC, abstractmethod
from json import dump
from os import makedirs
from shutil import rmtree
from shapely.geometry import Polygon, LineString, Point, mapping
from model.window import WindowMaker
from scipy.spatial import Delaunay
from itertools import permutations, combinations
from math import sqrt
import numpy as np
import rhino3dm as rh
from copy import deepcopy

def replace_nan_with_str(data_dict):
            for key in data_dict:
                if isinstance(data_dict[key], float) and data_dict[key] != data_dict[key]:
                    data_dict[key] = 'NaN'
                    
def coords_to_rhino_point(coords):
            return rh.Point(rh.Point3d(coords[0],coords[1],0))

def create_layer(doc:rh.File3dm, layer_name:str):
        layer = rh.Layer()
        layer.Name = layer_name
        doc.Layers.Add(layer)                    

class Element(ABC):

    doc_rh = rh.File3dm()

    @abstractmethod
    def build_to_rhino(self):
        pass

class BuildingElement(Element):
    
    FLOOR_HEIGHT = 4.0
    building_layer = rh.Layer()
    building_layer.Name = "Building"
    building_layer.Color = (255,0,0,255)
    building_layer_ind = Element.doc_rh.Layers.Add(building_layer)
    
    building_attr = rh.ObjectAttributes()
    building_attr.LayerIndex = building_layer_ind
    
    
    def __init__(self, dict_properties: dict):
        
        self.floor = dict_properties["층수"]
        self.name = dict_properties["주기"]
        self.type = dict_properties["종류"]
        self.usage = dict_properties["용도"]
        self.geometry_object = dict_properties["geometry"]
        self.geometry = mapping(dict_properties["geometry"]) #dict
        self.dictionary_prop = dict_properties
        self.extrusion_id = None # Guid
        
        replace_nan_with_str(self.dictionary_prop)
        self.dictionary_prop["geometry"] = self.geometry

    def build_to_rhino(self):
        if self.type == "무벽건물":
            return None
        coords = self.geometry['coordinates'][0]
        points = rh.Point3dList([rh.Point3d(coord[0],coord[1],0) for coord in coords])
        
        poly_line = rh.Curve.CreateControlPointCurve(points,1)
        if(poly_line.ClosedCurveOrientation() == rh.CurveOrientation.CounterClockwise):
            poly_line.Reverse()
            print("Reversed")
        extrusion = rh.Extrusion().Create(poly_line, -1 * self.floor * self.FLOOR_HEIGHT,True)
        
        self.extrusion_id = Element.doc_rh.Objects.AddExtrusion(extrusion,BuildingElement.building_attr)
        
                
    def __str__(self):
        return f"Building Element Object : Floor : {self.floor} | Name : {self.name} | Type : {self.type} | Usage : {self.usage}"

class VegetationElement(Element):
    
    vegetation_layer = rh.Layer()
    vegetation_layer.Name = 'Vegetation'
    vegetation_layer.Color = (0,255,0,255)
    vegetation_layer_ind = Element.doc_rh.Layers.Add(vegetation_layer)

    vegetation_attr = rh.ObjectAttributes()
    vegetation_attr.LayerIndex = vegetation_layer_ind
    
    def __init__(self, dict_properties: dict):
        self.geometry_object = dict_properties["geometry"]
        self.geometry = mapping(dict_properties["geometry"]) #dict
        self.dictionary_prop = dict_properties
        
        replace_nan_with_str(self.dictionary_prop)
        self.dictionary_prop["geometry"] = self.geometry

    def build_to_rhino(self):
        coord = self.geometry['coordinates']
        point = coords_to_rhino_point(coord)
    
        self.vegetation_id = Element.doc_rh.Objects.Add(point,VegetationElement.vegetation_attr)

class ContourElement(Element):
    
    #Class Properties
    resolution_of_division = 10
    divided_points = []
    curves = []
    
    contour_layer = rh.Layer()
    contour_layer.Name = 'Contour'
    contour_layer.Color = (0,0,255,255)
    contour_layer_ind = Element.doc_rh.Layers.Add(contour_layer)
    contour_obj_attr = rh.ObjectAttributes()
    contour_obj_attr.LayerIndex = contour_layer_ind
    
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

    @classmethod
    def __old_build_to_surface(cls):
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
            #Get sets of possible curves combinations in the same level
            reversed_curves = deepcopy(curves)
            for curves in reversed_curves : curves.Reverse()
            possible_curves = zip(curves,reversed_curves)
            
            for i in range(len(curves)+1):
                combs = list(combinations(range(len(curves)),i))
                curve_comb = []
                for i,comb in enumerate(combs): 
                    if i in comb:
                        curve_comb.append(curves[i])
                    elif i not in comb:
                        curve_comb.append(reversed_curves[i])
                connected_len(curve_comb)
                    
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
   
    @classmethod        
    def build_to_surface(cls):
        def __divide_curve(curve:rh.Curve,length:float):
            #Get Length of Curve
            if(isinstance(curve,rh.LineCurve)):
                crv_len = curve.Line.Length
            else:
                crv_len = curve.ToPolyline().Length
            
            #Divide Curve by approximate length
            div_num = int(crv_len/length)
            if div_num == 0:
                div_num = 1
           
           #Get Points of Curve by dividing parameters 
            points = [] 
            for i in range(div_num+1):
                
                new_pt = curve.PointAt(i/div_num * curve.Domain.T1)
                points.append((new_pt.X,new_pt.Y,new_pt.Z))

            return points
        
        def __project_pt_to_XY(pt):
            return (pt[0],pt[1])
        
        def __check_face_vertical(face_indices:list):
            #Get Face Vertices
            [ContourElement.divided_points[index] for index in face_indices]
            point_A = ContourElement.divided_points[face_indices[0]]
            point_B = ContourElement.divided_points[face_indices[1]]
            point_C = ContourElement.divided_points[face_indices[2]]
            vect_AB = [a_coord - b_coord for a_coord,b_coord in zip(point_A,point_B)]
            vect_AC = [a_coord - c_coord for a_coord,c_coord in zip(point_A,point_C)]
            if np.cross(vect_AB,vect_AC)[2] <= 1:
                return True
            else:
                return False
        
        def __remove_duplicates(point_list):
            unique_points = set()
            result = []
            
            for point in point_list:
                if point not in unique_points:
                    unique_points.add(point)
                    result.append(point)
            
            return result  
        
        #Get Divided Points
        crvs = ContourElement.curves
        ContourElement.divided_points = []
        for crv in crvs: ContourElement.divided_points.extend(__divide_curve(crv,ContourElement.resolution_of_division))
        #Adjust Border Points
        ##Get contour_curves' end points
        crv_end_pts_list = [crv.PointAtEnd for crv in crvs] + [crv.PointAtStart for crv in crvs]
        crv_end_pts = rh.PointCloud()
        for pt in crv_end_pts_list: crv_end_pts.Add(pt)
        ##Find closest point to each border point
        for border_pt in BorderElement.coords:
            closest_pt_ind = crv_end_pts.ClosestPoint(rh.Point3d(*border_pt))
            closest_pt = crv_end_pts.PointAt(closest_pt_ind)
            border_pt = list(border_pt)
            border_pt[2] = closest_pt.Z
            border_pt = tuple(border_pt)
            ContourElement.divided_points.append(border_pt)
        
        #Remove Duplicates
        ContourElement.divided_points = __remove_duplicates(ContourElement.divided_points)
        
        #Get Face Indices by scipy.spatial.Delaunay
        projected_points = [__project_pt_to_XY(pt) for pt in ContourElement.divided_points]
        face_indices = Delaunay(np.array(projected_points)).simplices
        
        #Create Mesh + filter vertical faces
        contour_mesh = rh.Mesh()
        for pt in ContourElement.divided_points: 
            contour_mesh.Vertices.Add(*pt)
        for face in face_indices:
            if not __check_face_vertical(face):
                contour_mesh.Faces.AddFace(*face)
        
        #Add to Document
        
        ContourElement.mesh_id = Element.doc_rh.Objects.AddMesh(contour_mesh,ContourElement.contour_obj_attr)
        # Element.doc_rh.Objects.AddMesh(contour_mesh)
        
class RoadElement(Element):
    
    road_layer = rh.Layer()
    road_layer.Name = 'Road'
    road_layer_ind = Element.doc_rh.Layers.Add(road_layer)
    
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
        
        self.road_id = Element.doc_rh.Objects.AddCurve(curve)
        Element.doc_rh.Objects.FindId(self.road_id).Attributes.LayerIndex = RoadElement.road_layer_ind

class BorderElement(Element):
    
    border_layer = rh.Layer()
    border_layer.Name = 'Border'
    border_layer.Color = (255,255,0,255)
    border_layer_ind = Element.doc_rh.Layers.Add(border_layer)
    
    def __init__(self, dict_properties: dict):
        self.geometry_object = dict_properties["geometry"]
        self.geometry = mapping(dict_properties["geometry"])
        BorderElement.coords = [(coord[0],coord[1],0) for coord in list(self.geometry['coordinates'])[:-1]]
        
    def build_to_rhino(self):
        coords = self.geometry['coordinates']
        points = [rh.Point3d(coord[0],coord[1],0) for coord in coords]
        curve = rh.Curve.CreateControlPointCurve(points,1)
        
        obj_attr = rh.ObjectAttributes()
        obj_attr.LayerIndex = BorderElement.border_layer_ind
        self.border_id = Element.doc_rh.Objects.AddCurve(curve,obj_attr)