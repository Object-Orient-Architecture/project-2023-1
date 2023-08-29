#Python Library
from zipfile import ZipFile
from os import path
import subprocess

#Custom Library and modules
from constants.options import *
from operator import Operator

class SiteModelingAutomation:
  '''
  SiteModelingAutomation(SMA) class is about the whole application
  Application's process consists of three step
  1. Getting <Zip File> containing SHP files from NGII and some options clients want to set
  2. Operate automated modeling process with Operator class Object following options and given file directory. Finally generate building brep, contour surface, road curve, vegetation point.
  3. Open 3dm file of result and run post-process(Running Rhino-inner script - Contour the surface and project all elements onto the contour surface)
  '''
  #0. Application Properties
  def __init__(self):
      self.options = {} #type : Map<String,Options(Enum)>
      self.zip_file = None #type : ZipFile (from zipfile)
      self.operator = Operator()
    
  #1. Get Options and zipfile
  def set_options(...):
    self.options = {"contour_type":ContourType.Surface,[,...]}
  
  #1. Get File
  def set_file(self, zip_file : ZipFile):
    self.zip_file = zip_file
  
  #2. Operate whole process
  def operate(self):
    operator = self.operator
    try:
      # 1 . make /.temp" directory and unzip whole file into the directory
      operator.unzip(self.zip_file) 

      # 2 . find each elements which is needed when making a site modeling from corresponding				    unzipped SHP files. 
      operator.find_elements() #Contain processes b
      '''
      operator.find_element("BUILDING") 	| #type : .shp File -> BuildingElement Class Object 
      operator.find_element("ROAD") 		| #type : .shp File -> RoadElement Class Object
      operator.find_element("VEGETATION") | #type : .shp File -> VegetationElement Class Object
      operator.find_element("CONTOUR") 	| #type : .shp File -> ContourElement Class Object
      operator.find_element("BORDER") 	| #type : .shp File -> BorderElement Class Object
      '''
      # 3 . Make a result.3dm document and add object parsed from each elements object above
      operator.bake_element_to_rhino()
      '''
      rhino_doc = rhino3dm.File3dm() 		| make rhino document
      building_elements.build_to_rhino()  | build all building elements into rhino document
      road_elements.build_to_rhino()		| same for road elements
      (... #same for other elements) 		| repetition
      '''
    except Exception as e:
      exception_msg = "Look up for file's validity or check whether the path is right"
      print(exception_msg)
      raise Exception(exception_msg)
    finally:
      operator.remove_unzipped() # Unconditionally remove unzipped file to prevent from wasted 										   memory
      
  #3. Open Rhino and post-process
  def get_result(self):
    rhino_exe_path = "path of Rhino.exe in the directory"
    # unconditionally choose result.3dm even if the project directory differs
    result_3dm = path.abspath('.\\main\\result\\result.3dm')
    postprocess_script = path.abspath(".\\main\\rhino_postprocess.py")
    # Run Rhino and open result.3dm after running postprocess scripts
    call_script = f'''
            "{rhino_exe_path} /nosplash 
            /runscript="-_RunPythonScript {postprocess_script} _OneView _Enter _SellAll 						_Zoom Selected", 
            "{result_3dm}"
                  '''
    subprocess.call(call_script)