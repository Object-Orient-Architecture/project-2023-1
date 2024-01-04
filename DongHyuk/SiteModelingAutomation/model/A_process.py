from zipfile import ZipFile
from model.constants.options import *
from model.B_sma_app import SMA

'''
전체 App에서 실행되는 프로세스
Client로부터 파일 경로와 사용하고자 하는 옵션을 전달받아
대지모형 어플리케이션을 실행시키는 역할
'''
class Proccess:
  def __init__(self,file_path:str,rhino_exe_path:str,rhino_doc_path:str):
    # App에서 입력받은 각 파일 경로들을 저장
    self.file_path = file_path # 지도 파일 경로
    self.rhino_exe_path = rhino_exe_path # Rhino 실행 파일 경로
    self.rhino_doc_path = rhino_doc_path # Rhino 문서 파일 저장 경로
  
  def call_sma(self) -> None:
    
    # 대지모형 어플리케이션 생성
    sma_app = SMA()
    
    # 대지모형 어플리케이션에 옵션 설정
    sma_app.set_options(
      building_type=BuildingType.NATURAL,
      vegetation_type=VegetationType.POINT,
      detail_type=DetailType.MASS,
      contour_type=ContourType.CONTOUR
    )
    
    # Client를 통해 입력받은 각 경로들을 대지모형 어플리케이션에 전달
    # 클라이언트의 진행 순서와 동일
    # 1. set_file :GeoJSON 파일 지정
    # 2. operate : Rhino 실행 파일을 지정하여 대지 모형의 기본적 Geometry 생성
    # 3. get_result: Rhino 문서를 열고 RhinoPythonScript 자동 실행을 통한 후처리
    file = ZipFile(self.file_path)
    sma_app.set_file(file) 
    sma_app.operate(self.rhino_doc_path)
    sma_app.get_result(self.rhino_doc_path,self.rhino_exe_path)