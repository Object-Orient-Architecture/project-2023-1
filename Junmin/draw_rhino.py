import rhino3dm as rh

class Model:
    """
    라이노 3dm파일을 지정합니다. 
    """

    def __init__(self):
        # type: () -> None

        self.file_dir = 'C:/Users/ERSATZ-CAMPUSTOWN/Documents/GitHub/project-2023-1/Junmin/rhino_md/rhino_temp.3dm'
        self.file3dm = rh.File3dm()
    def build_to_rhino(self):
        # type: () -> bool
        """
        라이노 파일을 작성합니다. 
        작성 성공시 True를 리턴합니다. 
        """
 
        bool = self.file3dm.Write(self.file_dir, 7)
        return bool
    
def coords_to_rhino_point(coords):
    # type: (list) -> rh.Point3d
    """
    좌표를 라이노 포인트로 전환합니다. 
    """

    return rh.Point3d(coords[0],coords[1],0)

class InterestPostProcess: 
    """
    흥미로운 주제의 리스트를 라이노로 굽는 과정을 정의하는 클래스 입니다. 
    """

    def __init__(self, model: Model,  interest_list:list):
        # type: (Model, list) -> None

        self.interest_list = interest_list
        self.model = model
    
    def build_to_rhino(self, heightdict, heightscale):
        # type: (dict, int) -> None
        """
        높이 데이터(얼마나 특이한지의 지표)와 높이의 배수를 입력하면 모델을 올립니다. 
        """

        for interest in self.interest_list:
            for polygon in interest.polygons:
                height = heightdict[interest.name]*heightscale
                coords = polygon.exterior.coords
                points = rh.Point3dList([coords_to_rhino_point(coord) for coord in coords])
                poly_line = rh.Curve.CreateControlPointCurve(points,1)

                attr = rh.ObjectAttributes()
                attr.Name = interest.name
                Extrusion_up = rh.Extrusion().Create(planarCurve = poly_line, height =  float(height), cap = True)
                Extrusion_down = rh.Extrusion().Create(planarCurve = poly_line,height = - float(height), cap = True)

                if (Extrusion_up is not None):
                    bbox = Extrusion_up.GetBoundingBox()
                    
                    bool = bbox.Center.Z > 0
                    if bool:
                        self.model.file3dm.Objects.AddExtrusion(Extrusion_up, attr)
                        
                    else:
                        self.model.file3dm.Objects.AddExtrusion(Extrusion_down, attr)
class BuildingPostProcess: 
    """
    흥미로운 건물의 리스트를 라이노로 굽는 과정을 정의하는 클래스 입니다. 
    """

    def __init__(self, model: Model, building_dict:dict):
        # type: (Model, dict) -> None

        self.building_dict = building_dict
        self.model = model

    def build_to_rhino(self, heightdict:dict, heightscale:int):
        # type: (dict, int) -> None
        """
        높이 데이터(얼마나 특이한지의 지표)와 높이의 배수를 입력하면 건물을 올립니다. 
        """

        def draw_coord_to_extrusion(polygon, height):
            coords = polygon.exterior.coords
            points = rh.Point3dList([coords_to_rhino_point(coord) for coord in coords])
            poly_line = rh.Curve.CreateControlPointCurve(points,1)
            Extrusion_up = rh.Extrusion().Create(planarCurve = poly_line, height =  float(height), cap = True)
            Extrusion_down = rh.Extrusion().Create(planarCurve = poly_line,height = - float(height), cap = True)
            if (Extrusion_up is not None):
                bbox = Extrusion_up.GetBoundingBox()
                bool = bbox.Center.Z > 0
                if bool:
                    self.model.file3dm.Objects.AddExtrusion(Extrusion_up)
                else:
                    self.model.file3dm.Objects.AddExtrusion(Extrusion_down)
        for name, buildings in self.building_dict.items():
            height = heightdict[name] * heightscale
            for building in buildings:
                polygon = building.polygon
                new_height= height * building.floor
                if polygon.geom_type == 'MultiPolygon':
                    for geom in polygon.geoms:
                        draw_coord_to_extrusion(geom, new_height)
                elif polygon.geom_type == 'Polygon':
                    draw_coord_to_extrusion(polygon, new_height)
                else:
                    pass