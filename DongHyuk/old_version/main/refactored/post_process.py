import rhinoscriptsyntax as rs

class RhinoProcessor:
  '''
  rhinoscriptsyntax와 같은 일부 Rhino Python API는 Rhino3D 소프트웨어에서만 실행 가능합니다.
  이 클래스는 Rhino3D에서만 실행 가능한 스크립트를 실행하기 위한 클래스입니다.
  SMA 어플리케이션에서 만들어진 요소들을 rhinoscriptsyntax를 활용해 후처리를 수행합니다.
  절차는 다음과 같습니다.
  1. SMA 어플리케이션에서 레이어별로 생성된 요소들을 변수로 받아옵니다.
  2. ContourType에 따라 등고 모형을 만들거나 면형 대지 Poly Surface를 생성합니다.
  3. 각 요소들을 등고선에 투영합니다.
  '''
  
  # 1 . 클래스 속성 Properties
  def __init__(self):
    '''
    SMA 어플리케이션이 분류해놓은 레이어별로 요소들을 받아옵니다.
    '''
    def __select_object_by_layer():
      return rs.ObjectsByLayer(layer)
  
    self.contour_mesh = __select_object_by_layer("Contour")
    self.road_crvs = __select_object_by_layer("Road")
    ... # vegetation_pts, and building_breps와 같은 다른 요소에 대해서도 반복
    
    #추가적으로 용이한 변형을 위해 mesh를 nurbs로 변환
    self.contour_srf = rs.MeshToNURB(self.contour_mesh)
    
  # 2 .옵션에 부합하는 대지 Poly Surface를 생성합니다.
  def process_contour(option:ContourType):
    '''
    어플리케이션이 생성한 등고면 메쉬와 사용자 지정 대지 옵션을 토대로 등고면을 만듭니다.
    등고면은 ContourType에 따라 면형 대지 또는 등고선 모형이 될 수 있습니다.
    결과로 Polysurface를 반환합니다.
    '''
    def __drape_and_contour(contour): #type : original surface -> contoured curves
      #...implementation
      return contour_crv
    
    def __solidize_surface(contour_srf): #type : origin surface -> polysurfaces having volume
      #...implementation
      return contour_polysrf
      
    def __extrude_contour(contour_crv): #type : contour curves -> extruded polysurfaces or extrusions
      #...세부 구현 생략 : 아래 코드는 개념화된 코드이며 실제 구현이 아님
      for crv in contour_crv: extrude(options.contour_height)
      return contour_polysrf
      
    if option == ContourType.Surface : self.contour_polysrf = __solidize_surface(self.contour_srf)
  elif option == ContourType.Contour : 
    self.contour_crv  	 = __drape_and_contour(self.contour_srf)
    self.contour_polysrf = __extrude_contour(self.contour_crv)
    
  # 3 . 다른 요소들을 대지 Polysurface에 투영합니다.
  # 3 - 1 . Building 요소를 투영합니다.
  def project_building():
    '''
    method __project()
    1. 건물 돌출 객체의 base curve를 구합니다.
    2. base curve의 꼭짓점들을 대지 면에 투영합니다.
    3. 투영된 점 중 가장 낮은 점을 찾아 건물 객체가 이동할 거리를 구합니다.
    4. 건물 Brep 객체를 #3에서 구한 값만큼 움직입니다.
    '''
    for building in self.building_breps:
    	#...implementation : code below is not real implementation but conceptualized psuedo code
		__project(building,self.contour_polysrf)
        
        
  # 3 - 2 . Vegetation 요소를 투영합니다.    
  def project_vegetation():
    Z_AXIS = (0,0,1)
    self.vegetation_pts = rs.ProjectPointToMesh(self.vegetation_pts,
                                                self.contour_polysrf,
                                                Z_AXIS)
  # 3 - 3 . Road 요소를 투영합니다.
  def project_road():
    '''
    method __project()의 세부 구현 내용
    1. 대지 Poly Surface의 옵션에 따라 다른 절차를 수행합니다.
   	if contourType == surface:
    	2. 도로를 나타내는 커브를 모두 합칩니다.(CurveBooleanUnion)
        3. 합쳐진 커브를 대지 면에 투영합니다.
        4. 대지 면을 복사하고 투영된 커브로 Split하여 도로면을 획득합니다.
        5. 도로면에 두께를 줍니다.
    elif contourType = Contour:
    	2. 도로를 나타내는 커브를 모두 합칩니다.(CurveBooleanUnion)
        3. 합쳐진 커브를 대지 등고선을 기준으로 Split하여 도로면을 획득합니다.
        4. 생성된 도로면들을 대지 면에 투영합니다.
        5. 도로면에 두께를 줍니다.
    '''
    __project(self.road_crvs, self.contour_polysrf)
    
processor = RhinoProcessor()
processor.process_contour(options)
processor.project_building()
processor.project_vegetation()
processor.project_road()