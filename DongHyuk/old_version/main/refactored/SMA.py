#Python Library
from zipfile import ZipFile
from os import path
import subprocess

#Custom Library and modules
from constants.options import *
from operator import Operator

class SiteModelingAutomation:
  '''
  SiteModelingAutomation(SMA) 클래스는 대지 모형 객체를 만들어 사용자에게 제공하는 인터페이스입니다.
  해당 어플리케이션은 3가지 단계로 작동됩니다.
  1. 국토정보플랫폼에서 얻은 SHP파일이 포함된 .zip파일과 사용자 옵션을 받습니다.
  2. 입력받은 파일과 옵션을 토대로 Operator 클래스 오브젝트를 통해 자동화된 사이트 모델링 프로세스를 수행합니다. 이 	 과정에서 건물, 도로, 식생, 등고선, 경계선을 추출합니다.
  3. 추출된 결과를 Rhino3D로 열어서 후처리를 수행하고 사용자에게 보여줍니다.(Rhino3D 내부 스크립트를 실행시켜서 등	  고선을 만들고, 모든 요소를 등고면에 투영합니다.)
  '''
  #0. 어플리케이션 속성(Properties)
  def __init__(self):
      self.options = {} #type : Map<String,Options(Enum)>
      self.zip_file = None #type : ZipFile (from zipfile)
      self.operator = Operator()
    
  #1. 옵션 설정
  def set_options(...):
    self.options = {"contour_type":ContourType.Surface,[,...]}
  
  #1. 파일 지정
  def set_file(self, zip_file : ZipFile):
    self.zip_file = zip_file
  
  #2. 입력받은 파일과 옵션을 토대로 자동화된 사이트 모델링 프로세스를 수행
  def operate(self):
    operator = self.operator
    try:
      # 1 . './temp'폴더를 생성하고 압축파일을 풀어서 해당 폴더에 저장
      operator.unzip(self.zip_file) 

      # 2 . 사이트 모델링을 만드는데 필요한 요소들을 상응하는 SHP파일에서 찾아 저장
      operator.find_elements() #아래 절차를 포함함
      '''
      operator.find_element("BUILDING")   | #type : .shp File -> BuildingElement Class Object 
      operator.find_element("ROAD") 	  | #type : .shp File -> RoadElement Class Object
      operator.find_element("VEGETATION") | #type : .shp File -> VegetationElement Class Object
      operator.find_element("CONTOUR") 	  | #type : .shp File -> ContourElement Class Object
      operator.find_element("BORDER") 	  | #type : .shp File -> BorderElement Class Object
      '''
      # 3 . result.3dm 파일을 생성하고 #2에서 찾은 요소들을 파일에 추가함
      operator.bake_element_to_rhino() #아래 절차를 포함함
      '''
      rhino_doc = rhino3dm.File3dm() 		| Rhino 파일 생성
      building_elements.build_to_rhino()    | 건물 요소를 Rhino 파일에 추가
      road_elements.build_to_rhino()		| 도로 요소도 동일하게 추가
      (... #same for other elements) 		| 다른 요소들에 대해서도 반복
      '''
    except Exception as e: # 파일을 읽는 과정에서 오류가 발생하면 오류 메시지를 출력하고 프로그램 종료
      exception_msg = "Look up for file's validity or check whether the path is right"
      print(exception_msg)
      raise Exception(exception_msg)
    finally:
      operator.remove_unzipped() #  메모리 낭비를 막기 위해 무조건적으로 압축 해제된 파일들을 삭제함
      
  #3. 라이노를 열고 후처리 수행
  def get_result(self):
    rhino_exe_path = "path of Rhino.exe in the directory"
    # 프로그램 디렉토리와 관계 없이 result.3dm을 열음
    result_3dm = path.abspath('.\\main\\result\\result.3dm')
    postprocess_script = path.abspath(".\\main\\rhino_postprocess.py")
    # Run Rhino and open result.3dm after running postprocess scripts
    call_script = f'''
            "{rhino_exe_path} /nosplash 
            /runscript="-_RunPythonScript {postprocess_script} _OneView _Enter _SellAll 						_Zoom Selected", 
            "{result_3dm}"
                  '''
    # subprocess.call()을 통해 result.3dm을 열고 후처리를 수행, 생성된 객체에 zoom
    subprocess.call(call_script)