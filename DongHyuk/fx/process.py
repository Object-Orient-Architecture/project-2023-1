# -*- coding:utf-8 -*-

import pickle
from sma_app import *
from app_operator import Operator

def get_building_elements():
        #1 | Get Input

        ##1 . 1 | Get Target Path
        zip_path = "data_src\\376120562 - 학교 + 산지\\(B010)수치지도_376120562_2022_00000642796721.zip"
        # zip_path = 'data_src\\376120531- 입구역 + 주거\\(B010)수치지도_376120531_2022_00000253813277.zip'

        ##1 . 2 | Get Application Options
        building_type = BuildingType.FLOOR
        doParapet = False
        contour_type = ContourType.CONTOURE
        vegetation_type = VegetationType.POINT

        #2 | Initialize App
        app = SMAApp(zip_path,building_type,doParapet,contour_type,vegetation_type)

        #3 | Operate App following inputs
        return app.operate()

        #4 | Save Output into specific drectory
        # app.get_result()
        
building_elements = get_building_elements()


with open('building_elements_list.pkl','wb') as f:
        pickle.dump(building_elements,f)
