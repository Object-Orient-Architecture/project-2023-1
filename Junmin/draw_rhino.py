import rhino3dm as rh

class Model:
    def __init__(self):
        self.file_dir = 'C:/Users/ERSATZ-CAMPUSTOWN/Documents/GitHub/project-2023-1/Junmin/rhino_md/rhino_temp.3dm'
        self.file3dm = rh.File3dm()
    def build_to_rhino(self):
        bool = self.file3dm.Write(self.file_dir, 7)
        return bool

def coords_to_rhino_point(coords):
    return rh.Point3d(coords[0],coords[1],0)

class InterestPostProcess: 
    def __init__(self, model: Model,  interest_list:list):
        self.interest_list = interest_list
        self.model = model
    
    def build_to_rhino(self, heightdict, heightscale):
        for interest in self.interest_list:
            for polygon in interest.polygons:

                height = heightdict[interest.name]*heightscale


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

class BuildingPostProcess: 
    def __init__(self, model: Model, building_dict:dict):
        self.building_dict = building_dict
        self.model = model
    
    def build_to_rhino(self, heightscale:int, heightdict:dict ):
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



