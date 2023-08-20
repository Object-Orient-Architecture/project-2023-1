from zipfile import ZipFile
from os import path
from enum import Enum
from elements import *
import pandas as pd
import geopandas as gpd

class Operator:
        
        __unzip_dir_name = '\\.temp'
        
        def __init__(self, zip_file : ZipFile):
                self.zip_file = zip_file
                self.zip_dir = path.dirname(self.zip_file.filename)
                self.unzip_dir = self.zip_dir + Operator.__unzip_dir_name
                
        def unzip(self):
                self.zip_file.extractall(self.unzip_dir)
        
        def find_elements(self):
                
                LayerIndex = {
                        'ROAD' : 'A001',
                        'BUILDING' : 'B001',
                        'WALL' : 'B002',
                        'CONTOUR' : 'F001'
                }
                        
                def __filter_file(layerIndex):
                        file_names = self.zip_file.namelist()        
                        layer_filenames = [name 
                                           for name in file_names 
                                           if layerIndex in name and name.endswith('.shp')]
                        
                        return [gpd.read_file(self.unzip_dir + '\\' + filename, encoding='euc-kr')
                                .to_dict(orient='records')
                                for filename in layer_filenames][0]
                
                def __list_layercode():
                        layer_code_csv = pd.read_csv('./layercode.CSV',encoding='euc-kr')
                        layer_code_name = layer_code_csv['Unnamed: 3']
                        layer_code_code = layer_code_csv['Unnamed: 4']
                        [print(str(i) + '\n') for i in zip(layer_code_name,layer_code_code)]
                    
                
                building_file = __filter_file(LayerIndex['BUILDING'])
                contour_file = __filter_file(LayerIndex['CONTOUR'])
                
                self.building_elements = [BuildingElement(building_info) for building_info in building_file]
                
                return self.building_elements
                # building_info = building_file[0]
                # print(building_info.keys())
                # temp_b = [(BuildingElement(v).height, print(i)) for i,v in enumerate(building_file)]
                
                
                
                
                
                

                
        

                
                
                