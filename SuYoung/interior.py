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
            "shelf" : ("shelf small", "shelf big","closet")
            }


# 가구 클래스
class Furniture:
    def __init__(self,Model=rg.GeometryBase):
        self.model = Model
        self.bbox = self.model.GetBoundingBox(rg.Plane.WorldXY)
        self.height = self.get_height()
        self.width,self.depth = self.get_width()
        self.axis = rg.Vector3d(0,-1,0)
            
    @property
    def area(self):
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
        self.bbox.Transform(trans)

    def rotate(self, angle):
        # angle을 받으면 해당 각도만큼 rotate
        # angle = degree (float)
        angle = math.radians(angle)
        trans = rg.Transform.Rotation(angle,self.position)
        self.model.Transform(trans)
        self.bbox.Transform(trans)
        self.axis.Transform(trans)
    
    @property
    def position(self):
        # 가구의 위치를 도출하는 함수
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
        
    def place():
        return

class Chair(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
    
    def place():
        return
        
class Shelf(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
    
    def place():
        return

class Bed(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
    
    def place(self,room):
        # 1. 모서리에 가구 배치
        point = room.wall[1][1]
        self.move(point)
        
        # 2. 방의 모양에 따라 축을 비교해 가구 회전
        # 2-1. 방이 가로형일 때: 축과 90도
        is_reverse = 1
        
        if (room.shape==1):
            target_axis = rg.Vector3d(-room.axis.Y,room.axis.X,0)
            test_pt = point + target_axis
            if(room.region.Contains(test_pt,rg.Plane.WorldXY,0)==rg.PointContainment.Coincident):
                is_reverse *= -1
        
        # 2-2. 방이 정방,세로형일 때: 축과 180도
        elif (room.shape==0):
            target_axis = -1 * room.axis
        
        dot_product = self.axis * target_axis
        angle_rad = math.acos(dot_product)
        degree = math.degrees(angle_rad * is_reverse)
        self.rotate(degree)
            
        #3. 벽에 붙도록 위치 조정
        corners = [rg.Point3d(pt) for pt in self.area.ToPolyline()]
        for pt in corners:
            if (room.region.Contains(pt,rg.Plane.WorldXY,0)==rg.PointContainment.Inside):
                self.move(pt)
        

# 방 클래스   
class Room:
    def __init__(self,plan=rg.Polyline):
        self.plan = plan                            # rg.Polyline
        self.door = rg.Line(plan.First,plan.Last)   # rg.Line
        self.wall = self.plan.GetSegments()         # [rg.Line]
        self.fur_type_list = []
        self.possible_region = plan
        self.placed_furniture=[]
    
    @property
    def wall(self):
        wall = self.plan.GetSegments()
        if (wall[0].Length<wall[-1].Length):
            wall.reverse()
        return wall
    
    @property
    def region(self):
        # 방의 영역을 도출하는 함수 
        points = list(self.plan)
        points.append(points[0])
        return  rg.PolylineCurve(points)

    def get_furniture_list(self):
        # 방의 타입에 맞는 가구를 클래스로 만들어 지정한 리스트에 저장하는 함수
        
        furniture_list = []
        
        for type in self.fur_type_list:
            model_data = data.BrepfromFilebyName(data.file_path,type)
            if model_data:
                furniture = Furniture(model_data)
                furniture = furniture.set_fur_type(type,type_table)
                furniture_list.append(furniture)
            else:
                print(type + "가구는 아직 준비되지 않았습니다.")
        
        return furniture_list
    
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
    
    @property
    def shape(self):
        if (self.depth >= self.width):
            return 0        # 세로형, 정방형
        else:
            return 1        # 가로형
        
    @property
    def width(self):
        return self.wall[2].Length
        
    @property
    def depth(self):
        return self.wall[1].Length
        
    @property
    def axis(self):
        # 방의 축을 반환한다.(축: 사람이 방 내부로 들어오는 방향) -> rg.Vector3D
        line = rg.Line(self.door[0],self.door[1])
        center = line.PointAt(0.5)
        trans = rg.Transform.Rotation(math.radians(90),rg.Vector3d.ZAxis,center)      
        line.Transform(trans)
        arrow = line[1] - line[0]
        if (self.region.Contains(line[0],rg.Plane.WorldXY,0) == rg.PointContainment.Inside):
            arrow *= -1
        arrow.Unitize()
        return  arrow

    def load(self):
        return [Bed(), Table()]
    
    def update_region(self, fur):
        self.possible_region

    @property
    def possible_region(self):
        # 플랜에서 placed furniture를 제외한 영역을 리턴한다.
        #self.plan self.placed_furniture
        return
    
    def generate(self,furnitures):
        for fur in furnitures:
            fur.place(self)
            self.placed_furniture.append(fur)
            self.update_region(fur)

class LivingRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.fur_type_list = ["sofa","coffe table","shelf small"]
               
class BedRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.fur_type_list = ["bed","desk","chair","closet"]
        
class Kitchen(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.fur_type_list = ["table","chair"]
        
class BathRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type

def set_room(plan,usage):
    
    room = Room(plan)
    typeroom = room.set_roomtype(usage)
    
    return typeroom