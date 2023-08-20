from options import BuildingType, VegetationType, ContourType
from zipfile import ZipFile


class SMA:
    '''
    class SMA (Object)
    SMA : Site Modeling Automation
    this class is an application for site modeling automation
    How to operate
    1. set options and file
    2. operate by Operator Object
    3. get result and save on local storage
    '''
    def __init__(self):
        self.options = {}
        self.zip_file = None

    def set_options(
        self,
        building_type: BuildingType = BuildingType.NATURAL,
        detailType: DetailType = DetailType.MASS,
        vegetation_type: VegetationType = VegetationType.POINT,
        contour_type: ContourType = ContourType.CONTOUR,
    ):
        self.options = {
            "building_type": building_type,
            "detailType": detailType,
            "vegetation_type": vegetation_type,
            "contour_type": contour_type,
        }

    def set_file(self, zip_file: ZipFile):
        self.zip_file = zip_file
    
    def operate(self):
        pass
    
    def get_result(self):
        pass
    
    