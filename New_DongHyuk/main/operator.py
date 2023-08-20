from os import path
from shutil import rmtree
from zipfile import ZipFile


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
        "CONTOUR": "F001",
    }

    # 2 | Properties
    def __init__(self):
        self.zip_file = None  # ZipFile Object
        self.zip_dir = ""  # path : path of zip_file

    # 3 | Methods
    # 3 - 0 | Set Zip File
    def set_zip_file(self, zip_file: ZipFile):
        self.zip_file = zip_file
        self.zip_dir = path.dirname(self.zip_file.filename)
        print(self.zip_dir)

    # 3 - 1 | Unzip File
    def unzip(self):
        unzip_path = self.zip_dir + self.__TEMP_UNZIP_DIR
        self.zip_file.extractall(unzip_path)

    # 3 - 2 | Find & Objectify Elements
    def find_elements(self, index: str):
        file_names = self.zip_file.namelist
        shp_names = [
            name
            for name in file_names
            if self.__LAYER_INDEX[index] in name and name.endswith(".shp")
        ]

        return shp_names

    # 3 - 3 | Bake Elements into Rhino Object

    # 3 - 4 | Save Rhino Object

    # 3 - 5 | Remove Unzipped File
    def remove_unzipped(self):
        unzip_path = self.zip_dir + self.__TEMP_UNZIP_DIR
        rmtree(unzip_path)


if __name__ == "__main__":
    operator = Operator()

    test_dir = "New_DongHyuk\\main\\data_src\\376120562 - 학교 + 산지\\(B010)수치지도_376120562_2022_00000642796721.zip"
    operator.set_zip_file(ZipFile(test_dir))
