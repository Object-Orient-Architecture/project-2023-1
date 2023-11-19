from os import path, makedirs, remove
from zipfile import ZipFile
import geopandas as gpd
import json
class Converter:
    
    # 상수
    __TEMP_UNZIP_DIR = "\\.temp"
    __LAYER_INDEX = {
        "ROAD": "A001",
        "BUILDING": "B001",
        "VEGETATION": "D003",
        "CONTOUR": "F0010000",
        "BORDER": "H001"
    }
    
    def __filter_shp(file_names:list):
            '''
            [입력]
            file_names : zip파일의 namelist(shp,spx 등이 포함되어있음, 위 요소들을 포함하는 shp파일만 필요)
            
            [출력]
            shp_names : 필요한 shp파일의 namelist
            '''
            shp_names = []
            for index in Converter.__LAYER_INDEX.values():
                shp_names.extend([
                    name
                    for name in file_names
                    if index in name and name.endswith(".shp")
                    
                ])  # 레이어 인덱스가 이름에 포함되어 있고 .shp파일 확장자인 것들로 구성
            return shp_names
        
    def __unzip(zip_file:ZipFile, zip_dir:str):
        '''
        [입력]
        zip_file : 압축해제할 zip파일의 ZipFile 객체
        zip_dir : 압축해제할 zip파일의 경로
        
        zip_file을 zip_dir에 압축해제한다.
        '''
        unzip_path = path.dirname(zip_dir) + Converter.__TEMP_UNZIP_DIR #임시경로 생성
        zip_file.extractall(unzip_path) #임시 경로에 압축해제
    
    def zip_to_data(self,zip_dir:str):
        '''
        [입력]
        zip_dir : zip파일의 경로
        
        경로의 zip파일을 __TEMP_UNZIP_DIR에 압축해제하고
        __LAYER_INDEX에 맞는 파일들을 불러와서
        가공가능한 Element 클래스의 객체들로 변환한다.
        데이터가 변환되면 압축해제한 파일은 삭제한다.
        '''
    
    
        #1 | 압축해제
        zip_file = ZipFile(zip_dir) #ZipFile 객체 생성
        Converter.__unzip(zip_file, zip_dir) #압축해제
        
        #2 | 필요 파일 추출
        file_names = zip_file.namelist() # nanme list에는 .shp, .shx 등이 포함되어있다.
        shp_names = Converter.__filter_shp(file_names) # 필요한 shp파일들만 추출
        
        #3 | shp파일을 Element 객체로 변환
        dict_geoinfos = [
            gpd.read_file(
                self.zip_dir + self.__TEMP_UNZIP_DIR + "\\" + shp_name, #파일명
                encoding="euc-kr", #인코딩
            ).to_dict(orient="records") #dict로 변환
            for shp_name in shp_names # shp파일들을
        ][0]  # SHP -> dict data list
        # 주의 : 읽은 파일은 가장 큰 컨테이너인 리스트를 포함하고 있으므로 제거가 필요하다.
        buildings = []
        roads = []
        vegetations = []
        contours = []
        border = None
        for index in Converter.__LAYER_INDEX.keys():
            if index == "BUILDING":
                buildings = [
                BuildingElement(info) for info in dict_geoinfos
                ]  # Return List<BuildingElement> from shp data
            elif index == "ROAD":
                    roads = [
                    RoadElement(info) for info in dict_geoinfos
                    ]  # Return List<RoadElement> from shp data
            elif index == "VEGETATION":
                    vegetations = [
                    VegetationElement(info) for info in dict_geoinfos
                    ]  # Return List<VegetationElement> from shp data
            elif index == "CONTOUR":
                    contours = [
                    ContourElement(info) for info in dict_geoinfos
                    ]  # Return List<ContourElement> from shp data
                    contours.sort(key=lambda x: x.elevation)
            elif index == "BORDER":
                    border = BorderElement(dict_geoinfos[0])
            


if __name__ == "__main__":
    target_path:str = r"C:\Users\Donghyeok\Downloads\(B010)수치지도_376082075_2022_00000552116528.zip"
    conv = Converter()
    conv.zip_to_data(target_path)