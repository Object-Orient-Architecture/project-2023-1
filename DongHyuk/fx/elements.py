from abc import ABC,abstractmethod
from Clients.client import SearchClient

class Element(ABC):
        
        @abstractmethod
        def build(self):
                pass

class BuildingElement(Element):
        
        ###SETTING###
        FLOOR_HEIGHT_CONST = 3.5
        
        def __init__(self, building_json:dict):
                self.type = building_json['종류']
                self.usage = building_json['용도']
                self.floor = building_json['층수']
                self.road_name = str(building_json['도로명'])
                self.main_address = str(building_json['건물본번'])
                self.sub_address = str(building_json['건물부번'])
                self.post_address = building_json['우편번호']
                self.geometry = building_json['geometry']

                address = self.road_name + ' ' + self.main_address + ' ' + self.sub_address

                # self.height = SearchClient.get_data_fromAddress(self.road_name + ' '
                #                                         + self.main_address + ' '
                #                                         + self.sub_address)[0]['properties']['HEIGHT']
                self.height = BuildingElement.FLOOR_HEIGHT_CONST * self.floor
                
        def build(self):
                pass


