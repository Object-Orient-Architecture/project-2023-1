import matplotlib.pyplot as plt
import import_address as addr

class Building:
    def __init__ (self, floor: int, polygon):
        self.floor = floor
        self.polygon = polygon

class Interest:
    def __init__ (self, name: str, polygons:list):
        self.name = name
        self.polygons = polygons

class AbnormalCheck:
    def __init__(self, seq_json: list, bbox:addr.BBoxFromCoordinate, nsdi_key:str, code_key:str):
        self.code_dict = addr.UsabilityCode(key = code_key).code_list
        self.interest_list = []

        matches = ["(연속주제)", "건물통합정보_마스터"]
        for seq in seq_json:
            if ("(연속주제)" in seq["OBJ_KNAME"]) or ("건물통합정보" in seq["OBJ_KNAME"]):
                self.check_loop(seq=seq, bbox=bbox, nsdi_key=nsdi_key, code_key=code_key)

    def check_loop(self, seq: dict, bbox:addr.BBoxFromCoordinate, nsdi_key:str, code_key:str):
        # seq를 훑으며 특이점을 찾습니다.

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
        
        if interest != 0:
            count = 0
            poly_list = []
            # 시퀀스에 값이 존재한다면, 이를 매트랩에 그리고 갯수를 호출합니다. 
            
            for poly_dict in polylist_seq:

                poly = poly_dict["polygon"]


                # prop = poly_dict["properties"]

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
                # current_BC = prop["BC_RAT"]
                # current_VL = prop["VL_RAT"]

                new_buiding = Building(floor=current_floor, polygon=poly)

                if current_use in use_dict:
                    use_dict[current_use].append(new_buiding)
                else:
                    use_dict[current_use] = [new_buiding]
            
                
            else:
                current_use = "미정"



            # if poly.geom_type == 'MultiPolygon':
            #     for geom in poly.geoms:
            #         plt.plot(*geom.exterior.xy)

            # elif poly.geom_type == 'Polygon':
            #     plt.plot(*poly.exterior.xy)

            # else:
            #     pass
        return use_dict