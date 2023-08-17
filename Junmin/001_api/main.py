import shapely
import import_address as addr
import matplotlib.pyplot as plt

# 주소와 키, 유저가 인풋하는 창구입니다.
your_address = "관천로 21"
your_geocoder_key = "27E280E5-0E68-3751-85C5-2802D1FA2BD1"
your_nsdi_key = "88c6b251809f4831a79145d085e07ded"

# 바운딩 박스의 반경 값입니다.
your_bound = 200


# 주소로 부터 좌표를 찾습니다.
coordinate = addr.CoordinateFromAddress(your_address, your_geocoder_key)

# 찾은 좌표를 바운딩 박스로 제작합니다. 
bbox = addr.BBoxFromCoordinate(coordinate.x, coordinate.y, your_bound)

seqjson = bbox.get_seq_data(key = your_nsdi_key)

print (seqjson)


# seq를 훑으며 특이점을 찾습니다. (함수화 할 예정....)
for seq in seqjson:
    name_seq = seq["OBJ_KNAME"] 
    geojson_seq = bbox.get_bbox_data(seq = seq["OBJ_SEQ"],key = your_nsdi_key)

    polylist_seq = bbox.get_polygon_properties(geojson_seq)

    if polylist_seq:

        area_seq = 0


        for poly_dict in polylist_seq:
            poly = poly_dict["polygon"]
            area_seq += poly.area
        
        # 특이구역 체크
        if "(연속주제)" in name_seq:
            interest = area_seq/bbox.area
        
            if interest != 0:
                count = 0

                # 시퀀스에 값이 존재한다면, 이를 매트랩에 그리고 갯수를 호출합니다. 
                for poly_dict in polylist_seq:
                    poly = poly_dict["polygon"]
                    prop = poly_dict["properties"]

                    if poly.geom_type == 'MultiPolygon':
                        for geom in poly.geoms:
                            plt.plot(*geom.exterior.xy)
                            count += 1
                    elif poly.geom_type == 'Polygon':
                        plt.plot(*poly.exterior.xy)
                        count += 1
                    else:
                        pass
                interest_found = "여기에는 {} 가 {}개 존재합니다.".format(name_seq, count)
                print (interest_found)
    else:
        pass
        
    # 건물군 체크
    #if "건물통합정보_마스터" in name_seq: or if "(도로명주소)" in name_seq: 
    # 도로 체크 



plt.show()


# ref4에서 보다 싶이 국소적으로 유의미한 정보는 
# (도로명주소) (연속주제) (건물통합정보-마스터)에 한정됩니다.
# 연속주제는 그중에서 특수한 정보를 담고 있으므로 따로 특이구역 체크를 진행하며
# 도로명 주소와 건물 통합 정보-마스터에 있는 건물의 용도와 면적, 도로의 면적 등의 정보를 체크
# 주소지 근처에 특이 건물의 개수, 주거환경의 차이 등을 확인합니다.

# 88c6b251809f4831a79145d085e07ded