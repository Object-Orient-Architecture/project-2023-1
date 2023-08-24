from os import path, makedirs, remove
from shutil import rmtree
from zipfile import ZipFile
import geopandas as gpd
import json


from elements import Element, RoadElement, BuildingElement, VegetationElement, ContourElement


class Operator:
    """
    class Operator(Object)
    this class do all the series of operations in a shape of method

    Operations
    1. Unzip File
    2. Find & Objectify Elements
    3. Bake Elements into Rhino Object
    4. Save Rhino Object
    5. Remove Upzipped File
    """

    # 1 | Constants

    __TEMP_UNZIP_DIR = "\\.temp"
    __LAYER_INDEX = {
        "ROAD": "A001",
        "BUILDING": "B001",
        "VEGETATION": "D003",
        "CONTOUR": "F0010000",
    }

    # 2 | Properties
    def __init__(self):
        self.zip_file = None  # ZipFile Object
        self.zip_dir = ""  # path : path of zip_file
        self.buildings = []  # List<BuildingElement>
        self.roads = []  # List<RoadElement>
        self.vegetations = []  # List<VegetationElement>
        self.contours = []  # List<ContourElement>

    # 3 | Methods
    # 3 - 0 | Set Zip File
    def set_zip_file(self, zip_file: ZipFile):
        self.zip_file = zip_file
        self.zip_dir = path.dirname(self.zip_file.filename)

    # 3 - 1 | Unzip File
    def unzip(self):
        unzip_path = self.zip_dir + self.__TEMP_UNZIP_DIR
        self.zip_file.extractall(unzip_path)

    # 3 - 2 | Find & Objectify Elements
    def find_elements(self, index: str):
        """
        throws Exception when index is not one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'
        """
        file_names = self.zip_file.namelist()  # namelist includes .shp, .shx and so on

        shp_names = [
            name
            for name in file_names
            if self.__LAYER_INDEX[index] in name and name.endswith(".shp")
        ]  # Filter shp files which is of index

        dict_geoinfos = [
            gpd.read_file(
                self.zip_dir + self.__TEMP_UNZIP_DIR + "\\" + shp_name,
                encoding="euc-kr",
            ).to_dict(orient="records")
            for shp_name in shp_names
        ][0]  # Convert shp Files into dict data list
        # CAUTION : readed file contains the largest container<List> which only has one element so that removing that is needed

        if index == "BUILDING":
            self.buildings = [
                BuildingElement(info) for info in dict_geoinfos
            ]  # Return List<BuildingElement> from shp data
        elif index == "ROAD":
            self.roads = [
                RoadElement(info) for info in dict_geoinfos
            ]  # Return List<RoadElement> from shp data
        elif index == "VEGETATION":
            self.vegetations = [
                VegetationElement(info) for info in dict_geoinfos
            ]  # Return List<VegetationElement> from shp data
        elif index == "CONTOUR":
            self.contours = [
                ContourElement(info) for info in dict_geoinfos
            ]  # Return List<ContourElement> from shp data
            self.contours.sort(key=lambda x: x.elevation)
        # Throws Exception when index is not one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'
        else:
            print(
                "Wrong Index | Please write one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'"
            )
            raise Exception(
                "Wrong Index | Please write one of 'BUILDING', 'ROAD', 'VEGETATION', 'CONTOUR'"
            )

    # 3 - 3 | Bake Elements into Rhino Object
    def bake_elements_tojson(self):
        dir_name = '.\\DongHyuk\\main\\.json_cache'
        elements = [self.roads, self.buildings, self.vegetations, self.contours]
        elements_name = ['roads','buildings','vegetations','contours']
        for i,element in enumerate(elements):
            if len(element) == 0:
                pass
            else:
                if(not path.isdir(dir_name)):
                    makedirs(dir_name)
                # Check if file already exists
                if path.isfile('{dir}/{name}.json'.format(dir = dir_name,name=elements_name[i])):
                    # Remove previous file
                    remove('{dir}/{name}.json'.format(dir = dir_name,name=elements_name[i]))
                    
                with open('{dir}/{name}.json'.format(dir = dir_name,name=elements_name[i]),'x') as json_file:
                    json.dump([elm.dictionary_prop for elm in element], json_file, indent=4,ensure_ascii=False)

    def bake_elements_to_rhino(self):
        # 3 - 3 - 1 | Bake Roads
        for road in self.roads:
            road.build_to_rhino()

        # 3 - 3 - 2 | Bake Buildings
        for building in self.buildings:
            building.build_to_rhino()

        # 3 - 3 - 3 | Bake Vegetations
        for vegetation in self.vegetations:
            vegetation.build_to_rhino()

        # 3 - 3 - 4 | Bake Contours
        for contour in self.contours:
            contour.build_to_rhino()
            
        ContourElement.build_to_surface()
        
    # 3 - 4 | Save Rhino Object
    def save_rhino_object(self):
        result_path = '.\\DongHyuk\\main\\result\\result.3dm'
        if(path.isfile(result_path)):
            remove(result_path)
        Element.doc_rh.Write(result_path,version=6)
        
    # 3 - 5 | Remove Unzipped File
    def remove_unzipped(self):
        unzip_path = self.zip_dir + self.__TEMP_UNZIP_DIR
        rmtree(unzip_path)


