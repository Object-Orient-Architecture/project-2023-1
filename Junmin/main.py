import shapely
import import_address as addr
import bbox_check as check
import draw_rhino as draw
import matplotlib.pyplot as plt
import compare_direction as cp

# 주소와 키, 유저가 인풋하는 창구입니다.
your_address = "관천로 21"
your_geocoder_key = "27E280E5-0E68-3751-85C5-2802D1FA2BD1"
your_nsdi_key = "88c6b251809f4831a79145d085e07ded"
your_code_key = "BNoOz%2BvJj4mb3cjDIrHx8%2FTWz0JeUmbBmpUWffNOwXmkUnOc21ivl6ra6OOcKby5wd0LNs9Eq6TzqvP34oZy7A%3D%3D"

# 바운딩 박스의 반경 값입니다.
your_bound = 200


# 주소로 부터 좌표를 찾습니다.
coordinate = addr.CoordinateFromAddress(your_address, your_geocoder_key)

# 찾은 좌표를 바운딩 박스로 제작합니다. 
bbox_centre = addr.BBoxFromCoordinate(coordinate.x, coordinate.y, your_bound)

north_coord = bbox_centre.north
south_coord = bbox_centre.south
east_coord = bbox_centre.east
west_coord = bbox_centre.west

bbox_north = addr.BBoxFromCoordinate(north_coord[0], north_coord[1], your_bound)
bbox_south = addr.BBoxFromCoordinate(south_coord[0], south_coord[1], your_bound)
bbox_east = addr.BBoxFromCoordinate(east_coord[0], east_coord[1], your_bound)
bbox_west = addr.BBoxFromCoordinate(west_coord[0], west_coord[1], your_bound)

seqjson_centre = bbox_centre.get_seq_data(key = your_nsdi_key)

print (seqjson_centre)


# seq를 훑으며 특이점을 찾습니다

# abnormal_centre = check.AbnormalCheck(seq_json=seqjson_centre, bbox=bbox_centre, nsdi_key=your_nsdi_key, code_key=your_code_key)

abnormal_north = check.AbnormalCheck(seq_json=seqjson_centre, bbox=bbox_north , nsdi_key=your_nsdi_key, code_key=your_code_key)
abnormal_south = check.AbnormalCheck(seq_json=seqjson_centre, bbox=bbox_south , nsdi_key=your_nsdi_key, code_key=your_code_key)
abnormal_west = check.AbnormalCheck(seq_json=seqjson_centre, bbox=bbox_west , nsdi_key=your_nsdi_key, code_key=your_code_key)
abnormal_east = check.AbnormalCheck(seq_json=seqjson_centre, bbox=bbox_east , nsdi_key=your_nsdi_key, code_key=your_code_key)



print ("특이한 점을 다 찾았습니다.")

# usability_centre = abnormal_centre.use_dict
# interests_centre = abnormal_centre.interest_list

usability_north = abnormal_north.use_dict
usability_south = abnormal_south.use_dict
usability_west = abnormal_west.use_dict
usability_east = abnormal_east.use_dict



interests_north = abnormal_north.interest_list
interests_south = abnormal_south.interest_list
interests_west = abnormal_west.interest_list
interests_east = abnormal_east.interest_list

usability_list = [usability_north,usability_south,usability_west,usability_east]
interests_list = [interests_north,interests_south,interests_west,interests_east]

dictcomp = cp.Comparison_dict(usability_list)
interecomp = cp.Comparison_interest(interests_list)

# 시각화 장치: 배수리스트를 넣으면 그 배수 만큼 그 용도를 높여주는 장치를 만들어보까

rhino3d = draw.Model()

for use in range(len(usability_list)):
    use_targetdict = dictcomp.dict_list[use]
    use_heightdict = dictcomp.compare_dicts(use)
    buildings_drawing = draw.BuildingPostProcess(rhino3d,use_targetdict)
    buildings_drawing.build_to_rhino(heightscale=20, heightdict=use_heightdict)

for inter in range(len(interests_list)):
    inter_targetdict = interecomp.interest_list[inter]
    inter_heightdict = interecomp.compare_interests(inter)
    interest_drawing = draw.InterestPostProcess(rhino3d,inter_targetdict)
    interest_drawing.build_to_rhino(heightscale=100, heightdict=inter_heightdict)
    
done = rhino3d.build_to_rhino()
print (done)





# rhino 파일로 제작하기



# plt.show()


# ref4에서 보다 싶이 국소적으로 유의미한 정보는 
# (도로명주소) (연속주제) (건물통합정보-마스터)에 한정됩니다.
# 연속주제는 그중에서 특수한 정보를 담고 있으므로 따로 특이구역 체크를 진행하며
# 도로명 주소와 건물 통합 정보-마스터에 있는 건물의 용도와 면적, 도로의 면적 등의 정보를 체크
# 주소지 근처에 특이 건물의 개수, 주거환경의 차이 등을 확인합니다.

# 88c6b251809f4831a79145d085e07ded