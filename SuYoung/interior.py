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
            "chair": ("chair", "sofa long", "sofa"),
            "bed" : "bed",
            "shelf" : ("shelf", "shelf long","closet")
            }


# 가구 클래스
class Furniture:
    def __init__(self,Model=rg.GeometryBase):
        self.model = Model
        self.bbox = self.model.GetBoundingBox(rg.Plane.WorldXY)
        self.area = self.get_area()
        self.height = self.get_height()
        self.width,self.depth = self.get_width()
        self.axis = rg.Vector3d(0,-1,0)        

    def get_area(self):
        '''
        가구의 바닥 면적을 폴리라인으로 도출하는 함수
        self -> rg.PolylineCurve
        '''
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
        '''
        가구의 상세타입을 입력하면 자동으로 클래스를 생성하는 함수
        fur_type : 가구의 상세타입, type_table : 타입을 정리한 테이블
        self , fur_type : str , type_table : dict -> Furniture
        '''
        
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
        '''
        위치를 입력받으면 해당 위치로 이동하는 함수
        self, location : rg.Point3D -> None
        '''
        move_vector = location - self.position
        trans = rg.Transform.Translation(move_vector)
        self.transform(trans)

    def Rotate(self, angle):
        '''
        각도를 입력받으면 해당 각도만큼 회전하는 함수
        self, angle : float -> None
        '''
        angle = math.radians(angle)
        trans = rg.Transform.Rotation(angle,self.position)
        self.transform(trans)
    
    def transform(self,transform):
        '''
        트랜스폼 매트릭스를 입력받으면 model, area, axis를 변형하는 함수
         self, transform : rg.Transform -> None
        '''
        self.model.Transform(transform)
        self.area.Transform(transform)
        self.axis.Transform(transform)
        self.axis.Unitize()

    def align_axis(self,target_axis=rg.Vector3d):
        '''
        목표 축을 입력하면 해당 축에 가구의 축을 정렬하는 함수
        self, target_axis : rg.Vector3D -> None
        '''
        trans =  rg.Transform.Rotation(self.axis,target_axis,self.position)
        self.transform(trans)
    
    @property
    def position(self):
        '''가구의 위치를 도출하는 함수'''
        return self.area.ToPolyline().CenterPoint()
    
    def get_height(self):
        '''가구의 높이를 도출하는 함수'''

        bbox = self.bbox
        corners = bbox.GetCorners()
        maxPt = max(corners,key=lambda x: x.Z)
        minPt = min(corners,key=lambda x: x.Z)
        
        return float(maxPt.Z - minPt.Z)
    
    def get_width(self):
        '''가구의 너비와 깊이를 도출하는 함수'''

        area = self.area.ToPolyline()
        lines = area.GetSegments()
        width = max(lines,key=lambda x:x.Length).Length
        depth = min(lines,key=lambda x:x.Length).Length
        return width,depth
    
    @property
    def region(self):
        '''
        가구의 점유 영역 (가구 영역 + 통로 900) 을 도출하는 함수
        self -> region : rg.PolylineCurve
        '''
        return self.area.Offset(rg.Plane.WorldXY,900,0,rg.CurveOffsetCornerStyle.Sharp)
    
    def arrange_to_Wall(self, region):
        '''
        영역에 걸쳐 배치된 가구를 영역에 맞춰주는 함수
        self, room : Room => bool
        '''
        corners = [rg.Point3d(pt) for pt in self.area.ToPolyline()]
        possible = []
        
        for pt in corners:
            if (region.Contains(pt,rg.Plane.WorldXY,0)==rg.PointContainment.Inside):
                possible.append(pt)

        if len(possible) == 1:
            point = possible[0]
        elif len(possible) > 1:
            point = rg.Polyline(possible).PointAt(0.5)
        else:
            return False
            
        if (point):
            self.move(point)
            return True
    
    def attatch_to_wall(self,region,point,target_axis):
        '''
        영역, 위치, 축을 입력하면 해당 위치와 축에 맞춰 방의 벽에 가구를 붙혀주는 함수
        self, region : rg.PolylineCurve, point : rg.Point3D, target_axis : rg.Vector3D -> None
        '''
        self.move(point)
        self.align_axis(target_axis)
        self.arrange_to_Wall(region)
    
class Table(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
        
    def place(self,room):
        # 책상일 경우
        if self.type == "desk":    
            self.place_desk(room)   
        
        # 커피 테이블일 경우
        elif self.type == "coffe table":
            self.find_sofa_long(room)

    def place_desk(self, room):
        '''
        방에 책상을 배치하는 함수
        '''
        # 1. 방의 모양에 따라 축을 비교해 가구 배치            
        # 1-1. 방이 가로형일 때: 축과 90도  
        if (room.shape==1):
            point = room.corner[0]
            target_axis = -1 * room.wall[0].Direction                       
            
        # 1-2. 방이 정방,세로형일 때: 축과 180도
        elif (room.shape==0):
            point = room.corner[2]
            target_axis = -1 * room.wall[1].Direction
        
        # 2. 배치
        self.attatch_to_wall(room.region,point,target_axis)
        
    def find_sofa_long(self,room):
        '''
        방에 배치된 긴 소파를 찾아 자동으로 배치하는 함수
        '''
        point,target_axis = (0,0)
        
        #1. 책상의 위치를 탐색하여 점과 방향 설정
        for fur in room.placed_furniture:
            if (fur.type == "sofa long"):
                point = fur.position + (fur.axis * (fur.depth/2 + self.depth/2 + 500)) 
                target_axis = fur.axis * -1
                
        #2. 이동 및 축 정렬
        if point and target_axis:
            self.move(point)
            self.align_axis(target_axis)        
            
class Chair(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
    
    def place(self,room):
        # 책상용 의자일 경우        
        if self.type == "chair":
            self.find_desk(room)
        
        # 긴 소파일 경우
        elif self.type == "sofa long":
            self.place_sofa_long(room)
        
        # 1인용 소파일 경우
        elif self.type == "sofa":
            self.find_coffe_table(room)

    def place_sofa_long(self, room):
        '''
        방에 긴 소파를 배치하는 함수
        '''
        #1. 소파가 놓일 벽을 찾아 중점과 축을 설정
        target_axis = room.valid_wall[1].Direction
        point = room.valid_wall[0].PointAt(0.5)
            
        #2. 이동
        self.attatch_to_wall(room.region,point,target_axis)
        
    def find_desk(self,room):
        '''
        방에 배치된 책상의 위치를 찾아 자동으로 배치하는 함수
        '''
        point,target_axis = (0,0)
        
        #1. 책상의 위치를 탐색하여 점과 방향 설정
        for fur in room.placed_furniture:
            if (fur.type == "desk"):
                point = fur.position + (fur.axis * (fur.depth/2 + self.depth/2 + 100)) 
                target_axis = fur.axis * -1
                
        #2. 이동 및 축 정렬
        if point and target_axis:
            self.move(point)
            self.align_axis(target_axis)
            
    def find_coffe_table(self,room):
        '''
        방에 배치된 커피 테이블을 찾아 자동으로 배치하는 함수
        '''
        point,target_axis = (0,0)
        
        #1. 책상의 위치를 탐색하여 점과 방향 설정
        for fur in room.placed_furniture:
            if (fur.type == "coffe table"):
                axis = fur.axis
                axis.Rotate(math.pi/2,rg.Vector3d(0,0,1))
                point = fur.position + (axis * (fur.width/2 + self.depth/2 + 500)) 
                target_axis = axis * -1
                
        #2. 이동 및 축 정렬
        if point and target_axis:
            self.move(point)
            self.align_axis(target_axis)
        
        
class Shelf(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
    
    def place(self,room):
        
        # 옷장일 경우
        if (self.type == "closet"):
            self.place_closet(room)
            
        # 긴 (낮은) 선반일 경우
        elif (self.type == "shelf long"):
            self.place_shelf_long(room)

    def place_shelf_long(self, room):
        '''
        길고 낮은 선반(티비 장)을 배치하는 함수
        '''
        #1. 선반이 놓일 벽을 찾아 위치와 축 설정
        point = room.valid_wall[-1].PointAt(0.5)
        target_axis = room.valid_wall[1].Direction * (-1)
        
        #2. 이동
        self.attatch_to_wall(room.region,point,target_axis)
            

    def place_closet(self, room):
        #1.방의 형상에 따라 가구 위치와 축 조정
        #1-1. 가로형일때
        if (room.shape ==1):
            point = room.corner[2]
            target_axis = room.wall[-1].Direction
                
        #1-2. 세로, 정방형 일때
        elif (room.shape ==0):
            point = room.corner[0]
            target_axis = room.wall[1].Direction
            
        #2.이동
        self.attatch_to_wall(room.region,point,target_axis)

class Bed(Furniture):
    def __init__( self, Model = rg.Brep, Type = str ):
        Furniture.__init__(self,Model)
        self.type = Type
    
    def place(self,room):
        #1. 모서리에 찾기
        point = room.corner[1]

        #2. 방의 형상에 따라 가구의 축 방향 정렬
        if (room.shape==1):
            target_axis = room.wall[2].Direction                          

        elif (room.shape==0):
            target_axis = -1 * room.wall[1].Direction

        #3. 이동
        self.attatch_to_wall(room.region,point,target_axis)      

# 방 클래스   
class Room:
    def __init__(self,plan=rg.Polyline):
        self.plan = plan                                # 평면 : rg.Polyline
        self.region = self.get_region()                 # 영역 : rg.PolylineCurve
        self.door = rg.Line(plan.First,plan.Last)       # 문 : rg.Line
        self.axis = self.get_axis()                     # 축 : rg.Vector3D
        self.wall = self.get_wall()                     # 벽 : [rg.Line]
        self.width = self.get_width()                   # 너비 : float
        self.depth = self.get_depth()                   # 깊이 : float
        self.shape = self.get_shape()                   # 형상 : int
        self.fur_type_list = []                         # 가구 타입 : [str]
        self.possible_region = self.init_region()       # 배치 가능 영역 : rg.PolylineCurve
        self.placed_furniture = []                      # 배치된 가구 : [rg.Brep]
        self.furnitures = []                            # 필요한 가구
    
    def init_region(self):
        '''
        방의 영역을 초기화 (방의 영역 - 문의 회전 영역) 하는 함수 
        self -> region : rg.PolylineCurve
        '''
        full_region = self.region
        if self.door.Length<1000:
            door_region = rg.PolylineCurve([self.door[0],self.door[1],self.door[1]+self.axis*self.door.Length,self.door[0]+self.axis*self.door.Length,self.door[0]])
            return rg.PolylineCurve.CreateBooleanDifference(full_region,door_region)[0]
        else:
            return full_region
        
    def get_wall(self):
        '''
        평면의 벽 선분을 도출하는 함수
        self -> [rg.Line]
        '''
        wall = self.plan.GetSegments()
        vect = wall[0].Direction
        vect.Unitize()
        if len(wall) == 5 and (wall[0].Length<wall[-1].Length):
            self.plan.Reverse()
        elif len(wall) == 4 and (vect == self.axis):
            self.plan.Reverse()
        wall = self.plan.GetSegments()
        return wall
    
    def get_region(self):
        '''
        방의 영역을 도출하는 함수 
        '''        
        points = list(self.plan)
        points.append(points[0])
        return  rg.PolylineCurve(points)

    def get_furniture_list(self):
        '''
        방의 타입에 맞는 가구를 클래스로 만들어 지정한 리스트에 저장하는 함수
        '''
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
    
    def set_roomtype(self,usage = int):
        '''
        입력받은 용도에 따라 방 클래스를 생성하는 함수
        usage : int => room : Room
        '''
        
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
        '''
        방의 형태를 반환하는 함수
        self -> shape: [int 0 : 세로,정방형 / int 1 : 가로형] 
        '''
        if (self.depth >= self.width):
            return 0        # 세로형, 정방형
        else:
            return 1        # 가로형
        
    def get_width(self):
        '''
        방의 너비를 반환하는 함수
        '''
        return float(self.wall[2].Length)
        
    def get_depth(self):
        '''
        방의 깊이를 반환하는 함수
        '''
        return float(self.wall[1].Length)
        
    def get_axis(self):
        '''
        방의 축을 반환하는 함수(축: 사람이 방 내부로 들어오는 방향) 
        self -> axis : rg.Vector3D
        '''
        line = rg.Line(self.door[0],self.door[1])
        center = line.PointAt(0.5)
        trans = rg.Transform.Rotation(math.radians(90),rg.Vector3d.ZAxis,center)      
        line.Transform(trans)
        arrow = line[1] - line[0]
        if (self.region.Contains(line[0],rg.Plane.WorldXY,0) == rg.PointContainment.Inside):
            arrow *= -1
        arrow.Unitize()
        return  arrow
    
    def update_region(self, fur):
        '''
        가구가 배치 가능한 영역을 갱신하는 함수
        self, fur : Furniture -> None 
        '''
        impossible_region = fur.area
        remain_region = rg.PolylineCurve.CreateBooleanDifference(self.possible_region,impossible_region)
        if(remain_region):
            self.possible_region = remain_region[0]

    
    def generate(self):
        '''
        방에 맞는 가구를 가상으로 배치하는 함수
        '''
        for fur in self.furnitures:
            fur.place(self)
            self.placed_furniture.append(fur)
            self.update_region(fur)
    
    def show(self):
        '''
        방의 가구를 라이노 상에 배치하는 함수
        '''
        return [fur.model for fur in self.placed_furniture]           

class LivingRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.fur_type_list = ["sofa long","coffe table","shelf long","sofa","shelf"]
        self.furnitures = self.get_furniture_list()
        self.valid_wall = self.set_wall()
        
    def set_wall(self):
        """
        벽들 중에 연산에 사용할 벽만 반환한다.
        Returns:
        self => valid_wall : [rg.Line]
        """
        if len(self.wall) == 5 :
            valid_wall = self.wall[1:-1]
        elif len(self.wall) == 4:
            valid_wall = self.wall[1:]
        else:
            valid_wall = self.wall
        return valid_wall
               
class BedRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.fur_type_list = ["bed","desk","chair","closet"]
        self.furnitures = self.get_furniture_list()
        self.corner = [self.wall[0][1],self.wall[1][1],self.wall[2][1],self.wall[3][1]]
        
class Kitchen(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.fur_type_list = ["table","chair"]
        self.furnitures = self.get_furniture_list()
        
class BathRoom(Room):
    def __init__(self,Plan=rg.Polyline,Type=str):
        Room.__init__(self,Plan)
        self.type = Type
        self.furnitures = self.get_furniture_list()

def set_room(plan=rg.Polyline,usage=int):
    '''
    평면과 용도를 입력하면 알맞은 방 객체를 생성하는 함수
    plan : rg.Polyline , usage : int => room : Room
    '''
    room = Room(plan)
    typeroom = room.set_roomtype(usage)
    if typeroom.depth < 2500 or typeroom.width < 2500:
        print("방이 너무 작습니다.")
        return None
    
    return typeroom