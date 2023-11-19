from model.constants.options import *
from zipfile import ZipFile
from model.operator_ import Operator
from os import path,mkdir,makedirs,remove
from shutil import copy
import subprocess


class SMA:
    '''
    class SMA (Object)
    SMA : Site Modeling Automation
    this class is an application for site modeling automation
    
    Operations
    1. set options and file
    2. operate by Operator Object
    3. get result and save on local storage
    '''
    #0 | Properties
    def __init__(self):
        self.options = {}
        self.zip_file = None
        self.operator = Operator()

    #1 | Methods
    
    #1 -1 | Set Methods
    def set_options(
        self,
        building_type: BuildingType = BuildingType.NATURAL,
        detail_type: DetailType = DetailType.MASS,
        vegetation_type: VegetationType = VegetationType.POINT,
        contour_type: ContourType = ContourType.CONTOUR,
    ):
        self.options = {
            "building_type": building_type,
            "detailType": detail_type,
            "vegetation_type": vegetation_type,
            "contour_type": contour_type,
        }

    def set_file(self, zip_file: ZipFile):
        self.zip_file = zip_file
    
    #1 -2 | Operate
    def operate(self, rhino_doc_path : str):
        try:
            self.operator.set_zip_file(self.zip_file)
            self.operator.unzip()
            self.operator.find_elements("BUILDING")
            self.operator.find_elements("CONTOUR")
            self.operator.find_elements("ROAD")
            self.operator.find_elements("VEGETATION")
            self.operator.find_elements("BORDER")
            self.operator.bake_elements_tojson()
            self.operator.bake_elements_to_rhino()
            self.operator.save_rhino_object(rhino_doc_path)
        except Exception as e:
            raise e
        finally:
            self.operator.remove_unzipped() # Unconditionally remove unzipped file
        
    #1 -3 | Get Result
    def get_result(self,rhino_doc_path:str, rhino_exe_path : str):
        file_to_open = rhino_doc_path+"\\result.3dm"
        script_to_copy_path = path.abspath(r".\model\rhino_postprocess.py")
        script_to_open = path.abspath(rhino_doc_path+"\\rhino_postprocess.py")
        try:
            copy_python_code(script_to_copy_path, rhino_doc_path)
            script_call = "-_RunPythonScript {0}".format(script_to_open)
            call_script = '"{0}"  /nosplash /runscript="{1} _OneView _Enter _SelAll _Zoom S ", "{2}"'.format(rhino_exe_path, script_call, file_to_open)
            subprocess.call(call_script)
            remove(script_to_open)
        finally:
            remove(script_to_open)



def copy_python_code(code_file, destination_dir):
    # 디렉토리가 존재하지 않을 경우 생성
    makedirs(destination_dir, exist_ok=True)

    # 코드 파일의 경로와 파일명 추출
    code_dir, code_filename = path.split(code_file)

    # 코드 파일을 목적 디렉토리로 복사
    copy(code_file, path.join(destination_dir, code_filename))

    print(f"{code_filename}을(를) {destination_dir}로 복사했습니다.")
    
    