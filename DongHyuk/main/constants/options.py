from enum import Enum

class BuildingType(Enum):
        NATURAL = 0
        FLOOR = 1
        
class VegetationType(Enum):
        POINT = 0
        PICTURE = 1
        MESH= 2

class DetailType(Enum):
        MASS = 0
        PARAPET = 1
        WINDOW = 2
        
class ContourType(Enum):
        CONTOUR = 0
        SURFACE = 1