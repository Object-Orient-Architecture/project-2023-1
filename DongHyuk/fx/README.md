# class SMAApp
- properties : __options , __file_path->zipFile, operator
- method : init, operate

# class Operator
- Input : shp_to_json:dict
- properties : BuildingElements, ContourElements, VegetElements, RoadElements, WaterElememts
- Methods : process below

# Process

1. Unzip
2. read_shp
3. find_building -> convert_buildingBase(into self.building_Elements
(iter. for each Elements)

4. BuildElements : get Options from App

5. Export 3dm and remove unzipped