from model.constants.options import *
from zipfile import ZipFile
from model.C_operator import Operator
from os import path,mkdir,makedirs,remove,getcwd,rmdir
from shutil import copy
import subprocess


class SMA:
    '''
    SMA : Site Modeling Automation
    대지모형 생성 어플리케이션
    '''
    #0 | 옵션, GeoJSON 파일 객체, 세부 구현을 수행할 Operator 객체를 초기화
    def __init__(self):
        self.options = {}
        self.zip_file = None
        self.operator = Operator()

    #1 | 구현 메소드
    '''
    1. set_options : 옵션 설정
    2. set_file : GeoJSON 파일 객체 설정
    3. operate : Operator 객체를 통해 대지모형
    '''
    
    #1 -1 | Set Methods
    def set_options(
        self,
        building_type: BuildingType = BuildingType.NATURAL,
        detail_type: DetailType = DetailType.MASS,
        vegetation_type: VegetationType = VegetationType.POINT,
        contour_type: ContourType = ContourType.CONTOUR,
    ) -> None:
        '''
        생성할 대지 모형의 옵션을 설정
        #TODO : 옵션 설정에 따른 Operator의 세부 작동 구현
        '''
        self.options = {
            "building_type": building_type,
            "detailType": detail_type,
            "vegetation_type": vegetation_type,
            "contour_type": contour_type,
        }
        print("SMA | 0 | 옵션 설정 완료")

    def set_file(self, zip_file: ZipFile) -> None:
        '''
        대지 모형을 생성할 GeoJSON 파일이 담긴 ZipFile 객체를 설정
        '''
        self.zip_file = zip_file
        print("SMA | 1 | GeoJSON 파일 설정 완료")
    
    #1 -2 | Operate
    def operate(self, rhino_doc_path : str) -> None:
        '''
        Operator 객체를 통해 입력된 경로에 대지모형이 생성된 Rhino 문서를 저장
        '''
        try:
            print("SMA | 2 | 대지모형 생성 시작")
            self.operator.set_zip_file(self.zip_file)
            self.operator.unzip()
            self.operator.find_elements("BUILDING")
            self.operator.find_elements("CONTOUR")
            self.operator.find_elements("ROAD")
            self.operator.find_elements("VEGETATION")
            self.operator.find_elements("BORDER")
            self.operator.bake_elements_to_rhino()
            self.operator.save_rhino_object(rhino_doc_path)
            print("SMA | 2 | 기초 대지모형 생성 완료")
        except Exception as e:
            #DEBUG
            print("SMA-operate에서 오류 발생\n 오류 내역 ---------- \n")
            import traceback as t
            t.print_exc()
            raise e
        finally:
            # 어떤 일이 있더라도 Unzip된 파일을 삭제
            self.operator.remove_unzipped()
        
    #1 -3 | Get Result
    def get_result(self,rhino_doc_path:str, rhino_exe_path : str):
        try:
            # RhinoPythonScript를 실행시키기 위해 복사할 파일 경로와 실행할 파일 경로를 설정
            file_to_open = rhino_doc_path + r"\result.3dm" # type: str
            script_to_copy_path = getcwd() + r"\model\rhino_postprocess.py" # type: str
            script_dir = r"C:\.tmpFileModeling" #type: str
            script_to_open = script_dir + r"\rhino_postprocess.py" # type: str
            
            # 일시적으로 Rhino 문서가 저장될 경로에 RhinoPythonScript를 복사
            copy_python_code(script_to_copy_path, script_dir)
            
            # RhinoPythonScript를 실행시키기 위한 명령어를 생성하고 실행
            print("SMA | 3 | 후처리 시작")
            script_call = "-_RunPythonScript {0}".format(script_to_open)
            call_script = '"{0}"  /nosplash /runscript="{1} _OneView _Enter _SelAll _Zoom S ", "{2}"'.format(rhino_exe_path, script_call, file_to_open)
            subprocess.call(call_script)
        except Exception as e:
            # 어떤 일이 있더라도 RhinoPythonScript를 복사한 파일을 삭제
            remove(script_to_open)
            rmdir(script_dir)
            
            # DEBUG
            print("SMA-get_result에서 오류 발생\n 오류 내역 ---------- \n")
            import traceback as t
            t.print_exc()
            raise e
        finally:
            # 어떤 일이 있더라도 RhinoPythonScript를 복사한 파일을 삭제
            remove(script_to_open)
            rmdir(script_dir)
            print("SMA | 3 | 후처리 완료")



def copy_python_code(code_file, destination_dir):
    # 디렉토리가 존재하지 않을 경우 생성
    makedirs(destination_dir, exist_ok=True)

    # 코드 파일의 경로와 파일명 추출
    code_dir, code_filename = path.split(code_file)

    # 코드 파일을 목적 디렉토리로 복사
    copy(code_file, path.join(destination_dir, code_filename))

    print(f"SMA | 3 | {code_filename}을(를) {destination_dir}로 복사했습니다.")
    
    