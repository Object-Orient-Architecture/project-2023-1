# 필수 세팅
#-*- coding: utf-8 -*-

try:
    from typing import List, Tuple
except:
    ImportError

import math

import Rhino.Geometry as rg  # type: ignore
import scriptcontext as sc  # type: ignore
import rhinoscriptsyntax as rs # type: ignore
import data

# 인풋
plan = None         # 평면 : rg.Polyline
usage = -1          # 용도 : int
fur_list = []       # 가구 : [rg.Brep]

# 가구 종류 정의
type_table = {
            "table": ("table", "desk", "coffe table") ,
            "chair": ("chair", "sofa big", "sofa small"),
            "bed" : "bed",
            "shelf" : ("shelf small", "shelf big")
            }

# 가구 클래스
class Furniture:
    def __init__(self,Model=rg.GeometryBase):
        self.model = Model
        self.bbox = Model.GetBoundingBox(rg.Plane.WorldXY)
        self.area = self.get_area()
        self.height = self.get_height()
        self.width,self.depth = self.get_width()
        self.position = self.get_center()
        
    def set_fur_type(self,fur_type,type_table = dict):
        # 가구의 상세타입을 입력하면 자동으로 클래스를 생성하는 함수
        # fur_type = 가구의 상세타입, type_table = 타입을 정리한 테이블
        
        for type in type_table:
            
            if fur_type in type_table[type]:
                
                if type == "table":
                    furniture = Table(self.model, fur_type)
                    
                elif type == "chair":
                    furniture = Chair(self.model, fur_type)
                    
                elif type == "bed":
                    furniture = Bed(self.model, fur_type)
                    
                elif type == "shelf":
                    furniture = Shelf(self.model, fur_type)
                    
        return furniture                
                           
    def move(self, location = rg.Point3d):
        # location을 받으면 해당 위치로 translate
        move_vector = location - self.position
        trans = rg.Transform.Translation(move_vector)
        self.model.Transform(trans)        
    
    def rotate(self, angle):
        # 라디안 angle 받아서 rotate
        raise NotImplementedError
    
    def place(self, room):
        # room 클래스를 받고 room의 컨디션을 활용해서
        # 배치를 잘 한다.
        raise NotImplementedError
    
    def get_area(self):        
        # 가구의 바닥 면적을 폴리라인으로 도출하는 함수
  
        bbox = self.bbox
        points = []
        floor = min(bbox.GetCorners(),key=lambda x: x.Z).Z
        for corner in bbox.GetCorners():
            if (corner.Z == floor):
                points.append(corner)
        points.append(points[0])
        area = rg.PolylineCurve(points)

        return area
    
    def get_center(self):
        return self.area.ToPolyline().CenterPoint()
    
    def get_height(self):
        # 가구의 높이를 도출하는 함수

        bbox = self.bbox
        corners = bbox.GetCorners()
        maxPt = max(corners,key=lambda x: x.Z)
        minPt = min(corners,key=lambda x: x.Z)
        
        return maxPt.Z - minPt.Z
    
    def get_width(self):
        # 가구의 너비와 깊이를 도출하는 함수

        area = self.area.ToPolyline()
        lines = area.GetSegments()
        width = max(lines,key=lambda x:x.Length).Length
        depth = min(lines,key=lambda x:x.Length).Length
        return width,depth
        
class Table(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type

class Chair(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
        
class Shelf(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type

class Bed(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type

# 방 클래스   
class Room:
    def __init__(self,plan=rg.Polyline):
        self.plan = plan                            # rg.Polyline
        self.door = rg.Line(plan.First,plan.Last)   # rg.Line
        self.wall = self.plan.GetSegments()         # [rg.Line]
        self.typelist = []
        self.possible_region = plan
        self.placed_furniture=[]
    
    def get_furniture_list(self):
        # 방의 타입에 맞는 가구를 클래스로 만들어 지정한 리스트에 저장하는 함수
        
        furniture_list = []
        
        for type in self.typelist:
            model_data = data.BrepfromFilebyName(data.file_path,type)
            if model_data:
                furniture = Furniture(model_data)
                furniture = furniture.set_fur_type(type,type_table)
                furniture_list.append(furniture)
            else:
                print(type + "가구는 아직 준비되지 않았습니다.")
        
        return furniture_list
    
    def get_area(self):
        points = list(self.plan)
        points.append(points[0])
        return  rg.PolylineCurve(points)
    
    def set_roomtype(self,usage):
        # 입력받은 용도에 따라 방 클래스를 생성하는 함수
        
        if( usage == 1 ):
            room_type = "거실"
            room = LivingRoom(self.plan,room_type)

        elif( usage == 2 ):
            room_type = "침실"
            room = BedRoom(self.plan,room_type)

        elif( usage == 3 ):
            room_type = "주방"
            room = Kitchen(self.plan,room_type)

        elif( usage == 4 ):
            room_type = "화장실"
            room = BathRoom(self.plan,room_type)

        return  room
    
    def get_shape(self):
        lines = self.plan.GetSegments()
        return lines

    def load(self):
        return [Bed(), Table()]
    
    def update(self, fur):
        self.possible_region
    @property
    def possible_region(self):
        # 플랜에서 placed furniture를 제외한 영역을 리턴한다.
        #self.plan self.placed_furniture
        return
    
    def generate(self):
        furnitures = self.load()
        for fur in furnitures:
            fur.place(self)
            self.placed_furniture.append(fur)
            self.update(fur)

class LivingRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.typelist = ["sofa","coffe table","shelf small"]
               
class BedRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.typelist = ["bed","desk","chair","shelf big"]
        
class Kitchen(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.typelist = ["table","chair"]
        
class BathRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type

def set_room(plan,usage):
    
    room = Room(plan)
    typeroom = room.set_roomtype(usage)
    
    return typeroom
