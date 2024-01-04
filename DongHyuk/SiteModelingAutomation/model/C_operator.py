from os import path, makedirs, remove
from shutil import rmtree
from zipfile import ZipFile
import geopandas as gpd
import json


from model.D_elements import Element, RoadElement, BuildingElement, VegetationElement, ContourElement, BorderElement


class Operator:
    """
    class Operator(Object)
    SMA에서 사용되는 대지모형 생성의 구현 클래스

    Operations
    1. Unzip File
    2. Find & Objectify Elements
    3. Bake Elements into Rhino Object
    4. Save Rhino Object
    5. Remove Upzipped File
    """

    # 1 | 상수
    __TEMP_UNZIP_DIR = "\\.temp"
    __LAYER_INDEX = {
        "ROAD": "A001",
        "BUILDING": "B001",
        "VEGETATION": "D003",
        "CONTOUR": "F0010000",
        "BORDER": "H001"
    }

    # 2 | 프로퍼티
    def __init__(self):
        self.zip_file = None  # GeoJSON이 담긴 압축파일 객체
        self.zip_dir = ""  # zip_file의 경로
        self.buildings = []  # BuildingElement 객체의 리스트
        self.roads = []  # RoadElement 객체의 리스트
        self.vegetations = []  # VegetationElement 객체의 리스트
        self.contours = []  # ContourElement 객체의 리스트

    # 3 | 작업
    # 3 - 0 | Zip File 설정
    def set_zip_file(self, zip_file: ZipFile) -> None:
        self.zip_file = zip_file
        self.zip_dir = path.dirname(self.zip_file.filename)
        print("Operator | 0 | Zip File 설정 완료")

    # 3 - 1 | Unzip File
    def unzip(self):
        unzip_path = self.zip_dir + self.__TEMP_UNZIP_DIR
        self.zip_file.extractall(unzip_path)
        print("Operator | 1 | Unzip File 완료")

    # 3 - 2 | Find & Objectify Elements
    def find_elements(self, index: str):
        """
        인덱스에 해당하는 shp 파일을 찾아서 해당 객체의 리스트를 Operator의 프로퍼티에 저장
        **인덱스가 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'가 아닐경우 예외발생
        """
        
        file_names = self.zip_file.namelist()  # shp 파일 이외에도 shx 등 다양한 파일이 포함되어 있음 
 
        shp_names = [
            name
            for name in file_names
            if self.__LAYER_INDEX[index] in name and name.endswith(".shp")
        ]  # shp 파일의 경로이름만 추출

        dict_geoinfos = [
            gpd.read_file(
                self.zip_dir + self.__TEMP_UNZIP_DIR + "\\" + shp_name,
                encoding="euc-kr",
            ).to_dict(orient="records")
            for shp_name in shp_names
        ][0]  # shp 파일을 geopandas로 읽어서 dictionary로 변환
        print("Operator | 2 | {index} 요소 추출 완료".format(index=index))
        print("Operator | 2 | {index} 요소의 개수 : {num}".format(index=index,num=len(dict_geoinfos)))
        print("Operator | 2 | 읽은 파일 : {dict_geoinfos}".format(dict_geoinfos=dict_geoinfos))
        # CAUTION : geopandas로 읽은 파일은 하나의 요소만을 갖는 리스트의 형식이므로 [0]으로 요소만 추출

        if index == "BUILDING":
            self.buildings = [
                BuildingElement(info) for info in dict_geoinfos
            ]  # Return List<BuildingElement> from shp data
            print("Operator | 2 | {index} 요소 객체화 완료".format(index=index))
            print("Operator | 2 | {index} 요소 객체의 개수 : {num}".format(index=index,num=len(self.buildings)))
        elif index == "ROAD":
            self.roads = [
                RoadElement(info) for info in dict_geoinfos
            ]  # Return List<RoadElement> from shp data
            print("Operator | 2 | {index} 요소 객체화 완료".format(index=index))
            print("Operator | 2 | {index} 요소 객체의 개수 : {num}".format(index=index,num=len(self.buildings)))
        elif index == "VEGETATION":
            self.vegetations = [
                VegetationElement(info) for info in dict_geoinfos
            ]  # Return List<VegetationElement> from shp data
            print("Operator | 2 | {index} 요소 객체화 완료".format(index=index))
            print("Operator | 2 | {index} 요소 객체의 개수 : {num}".format(index=index,num=len(self.buildings)))
        elif index == "CONTOUR":
            self.contours = [
                ContourElement(info) for info in dict_geoinfos
            ]  # Return List<ContourElement> from shp data
            self.contours.sort(key=lambda x: x.elevation) # 고도 순으로 정렬
            print("Operator | 2 | {index} 요소 객체화 완료".format(index=index))
            print("Operator | 2 | {index} 요소 객체의 개수 : {num}".format(index=index,num=len(self.buildings)))
        elif index == "BORDER":
            self.border = BorderElement(dict_geoinfos[0])
            print("Operator | 2 | {index} 요소 객체화 완료".format(index=index))
            print("Operator | 2 | {index} 요소 객체의 개수 : {num}".format(index=index,num=len(self.buildings)))
            
        # Throws Exception when index is not one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'
        else:
            print(
                "Wrong Index | Please write one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'"
            )
            raise Exception(
                "Wrong Index | Please write one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'"
            )

    # 3 - 3 | Bake Elements into Rhino Object
    # def bake_elements_tojson(self):
    #     dir_name = '.\\DongHyuk\\main\\.json_cache'
    #     elements = [self.roads, self.buildings, self.vegetations, self.contours]
    #     elements_name = ['roads','buildings','vegetations','contours']
    #     for i,element in enumerate(elements):
    #         if len(element) == 0:
    #             pass
    #         else:
    #             if(not path.isdir(dir_name)):
    #                 makedirs(dir_name)
    #             # Check if file already exists
    #             if path.isfile('{dir}/{name}.json'.format(dir = dir_name,name=elements_name[i])):
    #                 # Remove previous file
    #                 remove('{dir}/{name}.json'.format(dir = dir_name,name=elements_name[i]))
                    
    #             with open('{dir}/{name}.json'.format(dir = dir_name,name=elements_name[i]),'x') as json_file:
    #                 json.dump([elm.dictionary_prop for elm in element], json_file, indent=4,ensure_ascii=False)

    def bake_elements_to_rhino(self):
        # 3 - 3 - 1 | Bake Roads
        for road in self.roads:
            road.build_to_rhino()
            print("Operator | 3 | {index} 요소 Bake 완료".format(index="ROAD"))

        # 3 - 3 - 2 | Bake Buildings
        for building in self.buildings:
            building.build_to_rhino()
            print("Operator | 3 | {index} 요소 Bake 완료".format(index="BUILDING"))

        # 3 - 3 - 3 | Bake Vegetations
        for vegetation in self.vegetations:
            vegetation.build_to_rhino()
            print("Operator | 3 | {index} 요소 Bake 완료".format(index="VEGETATION"))

        # 3 - 3 - 4 | Bake Border
        self.border.build_to_rhino()
        print("Operator | 3 | {index} 요소 Bake 완료".format(index="BORDER"))
        
        # 3 - 3 - 5 | Bake Contours
        for contour in self.contours:
            contour.build_to_rhino()
            print("Operator | 3 | {index} 요소 Bake 완료".format(index="CONTOUR"))
        ContourElement.build_to_surface()
        print("Operator | 3 | {index} 요소 Bake 완료".format(index="CONTOUR-Surface"))
        
        
    # 3 - 4 | Save Rhino Object
    def save_rhino_object(self, rhino_doc_path : str):
        result_path = rhino_doc_path + "\\result.3dm"
        if(path.isfile(result_path)):
            remove(result_path)
        Element.doc_rh.Write(result_path,version=6)
        
    # 3 - 5 | Remove Unzipped File
    def remove_unzipped(self):
        unzip_path = self.zip_dir + self.__TEMP_UNZIP_DIR
        rmtree(unzip_path)


