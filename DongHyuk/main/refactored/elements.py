from abc import ABC, abstractmethod
from json import mapping
import rhino3dm

def create_layer(layer_name:str, layer_color:tuple) -> rhino3dm.ObjectAttributes:
  '''
  레이어를 이름과 색상을 지정하여 생성합니다.
  객체의 레이어를 설정하기 위해 사용되는 레이어 속성 객체를 반환합니다.
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
  모든 요소 클래스를 대표하는 추상 클래스입니다.
  모든 요소 클래스는 build_to_rhino() 메소드를 가져야 합니다.
  각 요소 클래스는 다른 속성을 가지고, 이것을 라이노 객체를 생성하는데 사용합니다.
  '''
  rhino_document = rhino3dm.File3dm() # 클래스 속성 : 모든 요소 클래스에서 접근가능한 라이노 파일 객체
  
  @abstractmethod
  def build_to_rhino(self)->None: 
    '''
    모든 요소 클래스에서 구현되며, 각 요소 클래스의 속성을 바탕으로 라이노 객체로 변환하는 메소드입니다.
    '''
    pass
  
class BuildingElement(Element):
  '''
  BuildingElement 클래스는 Element 클래스를 상속받아 build_to_rhino() 메소드를 가져야 합니다.
  클래스 상수 : floor_height - 한층의 높이, building_layer - 레이어 객체
  객체 속성 : floor - 층수, height - 건물 높이, base_geometry - 건물의 기본 도형
  '''
  
  FLOOR_HEIGHT = 4.0 # Class Properties : Constant
  BUILDING_LAYER = rhino3dm.Layer()
  BUILDING_LAYER.Name = "Building"
  
  def __init__(self,information_json):
    '''
    shp파일에서 읽은 json 데이터를 해석하여 객체의 속성으로 저장합니다.
    '''
    self.floor = information_json["층수"] #type:int
    self.height = FLOOR_HEIGHT * self.floor #type:float
	self.geometry = mapping(information_json["geometry"]) #type:dict(mapping함수 :json을 dictionary로 변환)
    
  def build_to_rhino(self):
    '''
    세부 구현 절차
    1. base curve의 꼭짓점 좌표를 가져옵니다.
    2. 꼭짓점 좌표를 바탕으로 Polyline<rhino3dm.Curve>를 생성합니다. 
    3. Polyline커브를 돌출시킵니다.(ExtrudeCrv)
    4. Element.rhino_document에 돌출된 면을 추가합니다. 레이어는 "Building"으로 설정합니다.
    '''
    #implementation
  
class VegetationElement(Element):
  '''	
  VegetaitionElement 클래스는 Element 클래스를 상속받아 build_to_rhino() 메소드를 가져야 합니다.
  객체 속성 : geometry<Point2d> - 수목의 위치
  '''
  def __init__(self,information_json):
    self.geometry = mapping(information_json["geometry"]) #type:dict
  
  def build_to_rhino(self):
    '''
    세부 구현 절차
    1. 수목의 위치를 가져옵니다. Z값은 0으로 두고 3차원 점으로 변환합니다.
    2. Element.rhino_document에 위치를 나타내는 점을 추가합니다. 레이어는 "Vegetation"으로 설정합니다.
    '''
	  coord = self.geometry['coordinates']
    point = rhino3dm.Point3d(coord[0],coord[1],0)
    
    # 객체를 파란색의 "Vegetation" 레이어에 추가합니다.
    Element.rhino_document.Objects.Add(point,create_layer("Vegetation",(0,0,255,255)))

class ContourElement(Element):
  '''	
  ContourElement 클래스는 Element 클래스를 상속받아 build_to_rhino() 메소드를 가져야 합니다.
  클래스 속성 : resolution_of_division - 등고면의 해상도, contour_curves - 등고선 커브들의 리스트
  객체 속성 : elevation - 등고선의 높이, base_geometry<List<Point2d>> - 등고선의 꼭짓점들
  클래스 함수 : build_to_surface(cls) - Delaunay 알고리즘을 이용하여 등고면을 만듭니다.
  '''	    
  #클래스 상수
  resolution_of_division = 10
  contour_curves = []
    
  def __init__(self, information_json):
    self.elevation = information_json["등고수치"] #type:float
    self.geometry = mapping(information_json["geometry"]) #type:dict 
  
  def build_to_rhino(self):
	  '''
    세부 구현 절차
    1. 등고선의 꼭짓점들을 가져와 Polyline<rhino3dm.Curve>를 생성합니다.
    2. 생성된 커브를 ContourElement.contour_curves에 추가합니다.
    '''
    #implementation
    
  @classmethod        
  def build_to_surface(cls):
    '''
    세부 구현 절차
    1. ContourElement.contour_curves의 커브들을 길이 기준으로 나누어 점을 생성합니다.
    2. 사이트 모델링의 경계 커브에서 꼭짓점을 가져오고, 해당 점들을 가장 가까운 대지 커브와 같은 높이로 이동시킵니다.
       이는 대지 면이 모델링의 경계까지 완전히 만들어지게 하기 위함입니다.
    3. 점들의 복사본을 만들고 XY-평면에 투영합니다.
    4. 투영된 2차원 점들에 Delaunay 알고리즘을 적용하여 생성될 메쉬 면의 인덱스를 구합니다.
    5. 위 절차에서 얻은 점들과 면의 인덱스들을 바탕으로 rhino3dm.Mesh 객체를 생성합니다.
    '''
    #...implementation above
    Element.rhino_document.Objects.Add(contour_mesh,create_layer("Contour",(255,0,0,255)))
    
class RoadElement(Element):
  '''
  RoadElement 클래스는 Element 클래스를 상속받아 build_to_rhino() 메소드를 가져야 합니다.
  객체 속성 : geometry<List<Point2d>> - 도로의 꼭짓점들
  build_to_rhino() 메소드는 BuildingElement의 메소드와 거의 동일하지만 레이어가 "Road"로 설정되고 돌출하지 않습니다.

  '''

class BorderElement(Element):
  '''
  RoadElement와 동일합니다.
  '''