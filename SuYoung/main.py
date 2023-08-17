#-*- coding: utf-8 -*-

try:
    from typing import List, Tuple
except:
    ImportError

import math

import Rhino.Geometry as rg  # type: ignore
import scriptcontext as sc  # type: ignore

# 가구 클래스
class Furniture:
    def __init__(self,Model=rg.GeometryBase):
        self.model = Model
    
    def get_area(self):
        dup = self.model.DuplicateBrep()
        vector = rg.Vector3d(0,0,-1)
        plane = rg.Plane.WorldXY
        trans = rg.Transform.ProjectAlong(plane,vector)
        dup.Transform(trans)
        area = dup
        return area
    
class Table(Furniture):
    def __init__(self,Model=rg.GeometryBase,Type=str):
        Furniture.__init__(self,Model)
        self.type = Type

class Chair(Furniture):
    def __init__(self,Model=rg.GeometryBase,Type=str):
        Furniture.__init__(self,Model)
        self.type = Type
        
class Shelf(Furniture):
    def __init__(self,Model=rg.GeometryBase,Type=str):
        Furniture.__init__(self,Model)
        self.type = Type

class Bed(Furniture):
    def __init__(self,Model=rg.GeometryBase,Type=str):
        Furniture.__init__(self,Model)
        self.type = Type
        
# 방 클래스   
class Room:
    def __init__(self,Plan=rg.Polyline):
        self.Plan = Plan
        self.door = rg.Line(Plan.First,Plan.Last)
        return
    
    def draw(self):
        return self.Plan
    
    def get_area(Plan):
        return

class LivingRoom(Room):
    def __init__(self,Plan,Type):
        Room.__init__(self,Plan)
        self.type = Type
        
class BedRoom(Room):
    def __init__(self,Plan,Type):
        Room.__init__(self,Plan)
        self.type = Type
        
class Kitchen(Room):
    def __init__(self,Plan,Type):
        Room.__init__(self,Plan)
        self.type = Type
        
class BathRoom(Room):
    def __init__(self,Plan,Type):
        Room.__init__(self,Plan)
        self.type = Type