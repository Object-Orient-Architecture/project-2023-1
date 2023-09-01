import matplotlib.pyplot as plt
import import_address as addr

class Building:
    """
    빌딩의 정보를 저장하는 클래스
    """

    def __init__ (self, floor: int, polygon):
        # type: (int, shapely.polygon) -> None

        self.floor = floor
        self.polygon = polygon

class Interest:
    """
    흥미로운 주제를 구성하는 구역을 저장하는 클래스
    """

    def __init__ (self, name: str, polygons:list):
        # type: (shapely.polygon, str) -> None
        
        self.name = name
        self.polygons = polygons

class AbnormalCheck:
    """
    특이한 지역과 특이한 건물들을 찾아주는 클래스입니다.
    """

    def __init__(self, seq_json: list, bbox:addr.BBoxFromCoordinate, nsdi_key:str, code_key:str):
       # type: (list, addr.BBoxFromCoordinate, str, str) -> None

        self.code_dict = addr.UsabilityCode(key = code_key).code_list
        self.interest_list = []

        matches = ["(연속주제)", "건물통합정보_마스터"]
        for seq in seq_json:

            if ("(연속주제)" in seq["OBJ_KNAME"]) or ("건물통합정보" in seq["OBJ_KNAME"]):
                self.check_loop(seq=seq, bbox=bbox, nsdi_key=nsdi_key, code_key=code_key)

    def check_loop(self, seq: dict, bbox:addr.BBoxFromCoordinate, nsdi_key:str, code_key:str):
        # type: (dict, addr.BBoxFromCoordinate, str, str) -> None
        """
        클래스가 정의되는 순간 바운딩박스를 돌며 특이지점을 찾습니다.
        """

        name_seq = seq["OBJ_KNAME"] 
        geojson_seq = bbox.get_bbox_data(seq = seq["OBJ_SEQ"],key = nsdi_key)
        polylist_seq = bbox.get_polygon_properties(geojson_seq)
        if polylist_seq:
            area_seq = 0
            for poly_dict in polylist_seq:
                poly = poly_dict["polygon"]
                area_seq += poly.area
            interest = area_seq/bbox.area
            # 특이구역 체크
            if "(연속주제)" in name_seq:
                interset_return = self.check_interest(name_seq, interest, polylist_seq)
                self.interest_list.append(interset_return)    
            elif "건물통합정보" in name_seq:
                print ("건물정보를 찾았습니다.")
                self.use_dict = self.check_building(name_seq, polylist_seq, code_key)
        else:
            pass
            
    def check_interest(self, name_seq, interest, polylist_seq):
        # type: (str, float, list[dict]) -> Interest
        """
        seq의 이름과 폴리곤의 속성과 형태가 주어지면 폴리곤의 개수를 샙니다. 
        """

        if interest != 0:
            count = 0
            poly_list = []

            # 시퀀스에 값이 존재한다면, 이를 매트랩에 그리고 갯수를 호출한다. 
            for poly_dict in polylist_seq:
                poly = poly_dict["polygon"]
                if poly.geom_type == 'MultiPolygon':
                    for geom in poly.geoms:
                        poly_list.append(geom)
                        plt.plot(*geom.exterior.xy)
                        count += 1
                elif poly.geom_type == 'Polygon':
                    poly_list.append(poly)
                    plt.plot(*poly.exterior.xy)
                    count += 1
                else:
                    pass
            interest_found = "여기에는 {} 가 {}개 존재합니다.".format(name_seq, count)
            found_interest = Interest(name= name_seq, polygons= poly_list)
            print (interest_found)
            return found_interest

    def check_building(self, name_seq, polylist_seq, code_key):
        # type: (str, list[dict], str) -> dict(str, Building)
        """
        건물정보 내의 폴리곤의 속성과 형태가 주어지면 건물 종류별 갯수를 샙니다. 
        """       

        use_dict = {}
        for poly_dict in polylist_seq:
            poly = poly_dict["polygon"]
            prop = poly_dict["properties"]
            code_key = prop["USABILITY"]
            if code_key :
                try:
                    current_use = self.code_dict[code_key]
                except:
                    current_use = "미정"
                try:
                    current_floor = int(prop["GRND_FLR"])
                except:
                    current_floor = 0
                new_buiding = Building(floor=current_floor, polygon=poly)
                if current_use in use_dict:
                    use_dict[current_use].append(new_buiding)
                else:
                    use_dict[current_use] = [new_buiding]
            else:
                current_use = "미정"
        return use_dict