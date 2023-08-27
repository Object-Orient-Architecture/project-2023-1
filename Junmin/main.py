import shapely
import import_address as addr
import bbox_check as check
import draw_rhino as draw
import matplotlib.pyplot as plt
import compare_direction as cp


your_address = "관천로 121"
your_geocoder_key = "27E280E5-0E68-3751-85C5-2802D1FA2BD1"
your_nsdi_key = "88c6b251809f4831a79145d085e07ded"
your_code_key = "BNoOz%2BvJj4mb3cjDIrHx8%2FTWz0JeUmbBmpUWffNOwXmkUnOc21ivl6ra6OOcKby5wd0LNs9Eq6TzqvP34oZy7A%3D%3D"

# 바운딩 박스의 반경 값입니다.
your_bound = 2000
class Main:
    def __init__(self) -> None:
        pass

    # 주소와 키, 유저가 인풋하는 창구입니다.
    def get_input_main (self, address: str, geocoder_key: str, nsdi_key: str, code_key: str, bound: int):
        self.address = address 
        self.geocode_key = geocoder_key
        self.nsdi_key = nsdi_key
        self.code_key = code_key
        self.bound = bound
    
    def get_four_direction_coord (self):
        # 주소로 부터 좌표를 찾습니다.
        self.coordinate_centre = addr.CoordinateFromAddress(self.address, self.geocode_key)
        # 찾은 좌표를 바운딩 박스로 제작합니다.
        self.bbox_centre = addr.BBoxFromCoordinate(self.coordinate_centre.x, self.coordinate_centre.y, self.bound)

        self.north_coord = self.bbox_centre.north
        self.south_coord = self.bbox_centre.south
        self.east_coord = self.bbox_centre.east
        self.west_coord = self.bbox_centre.west

    def get_four_direction_bbox (self):
        self.bbox_north = addr.BBoxFromCoordinate(self.north_coord[0], self.north_coord[1], self.bound)
        self.bbox_south = addr.BBoxFromCoordinate(self.south_coord[0], self.south_coord[1], self.bound)
        self.bbox_east = addr.BBoxFromCoordinate(self.east_coord[0], self.east_coord[1], self.bound)
        self.bbox_west = addr.BBoxFromCoordinate(self.west_coord[0], self.west_coord[1], self.bound)

        self.seqjson_centre = self.bbox_centre.get_seq_data(key = self.nsdi_key)

    def get_four_direction_abnormal(self):
        # seq를 훑으며 특이점을 찾습니다

        # abnormal_centre = check.AbnormalCheck(seq_json=seqjson_centre, bbox=bbox_centre, nsdi_key=your_nsdi_key, code_key=your_code_key)

        self.abnormal_north = check.AbnormalCheck(
            seq_json=self.seqjson_centre, 
            bbox=self.bbox_north ,
            nsdi_key=self.nsdi_key, 
            code_key=self.code_key
        )
        self.abnormal_south = check.AbnormalCheck(
            seq_json=self.seqjson_centre, 
            bbox=self.bbox_south , 
            nsdi_key=self.nsdi_key, 
            code_key=self.code_key
        )
        self.abnormal_west = check.AbnormalCheck(
            seq_json=self.seqjson_centre, 
            bbox=self.bbox_west , 
            nsdi_key=self.nsdi_key, 
            code_key=self.code_key
        )
        self.abnormal_east = check.AbnormalCheck(
            seq_json=self.seqjson_centre, 
            bbox=self.bbox_east , 
            nsdi_key=self.nsdi_key, 
            code_key=self.code_key
        )
        try:
            usability_north = self.abnormal_north.use_dict
        except:
            usability_north = False
        try:
            usability_south = self.abnormal_south.use_dict
        except:
            usability_south = False
        try:
            usability_west = self.abnormal_west.use_dict
        except:
            usability_west = False
        try:
            usability_east = self.abnormal_east.use_dict
        except:
            usability_east = False


        interests_north = self.abnormal_north.interest_list
        interests_south = self.abnormal_south.interest_list
        interests_west = self.abnormal_west.interest_list
        interests_east = self.abnormal_east.interest_list
        
        self.usability_list = []
        if usability_north:
            self.usability_list.append(usability_north)
        if usability_south:
            self.usability_list.append(usability_south)
        if usability_east:
            self.usability_list.append(usability_east)
        if usability_west:
            self.usability_list.append(usability_west)         
        self.interests_list = [interests_north,interests_south,interests_west,interests_east]
    
    def compare_four_direction(self):
        self.dictcomp = cp.Comparison_dict(self.usability_list)
        self.interecomp = cp.Comparison_interest(self.interests_list)

    def draw_four_direction(self):
        rhino3d = draw.Model()
        dictcomp = self.dictcomp
        interecomp = self.interecomp
        for use in range(len(self.usability_list)):
            use_targetdict = dictcomp.dict_list[use]
            use_heightdict = dictcomp.compare_dicts(use)
            buildings_drawing = draw.BuildingPostProcess(rhino3d,use_targetdict)
            buildings_drawing.build_to_rhino(heightscale=20, heightdict=use_heightdict)
            print (use_heightdict)

        for inter in range(len(self.interests_list)):
            inter_targetdict = interecomp.interest_list[inter]
            inter_heightdict = interecomp.compare_interests(inter)
            interest_drawing = draw.InterestPostProcess(rhino3d,inter_targetdict)
            interest_drawing.build_to_rhino(heightscale=100, heightdict=inter_heightdict)
            print (inter_heightdict)
            
        done = rhino3d.build_to_rhino()
        if (done):
            print ("비교에 성공했습니다.")

Mainpro = Main()
Mainpro.get_input_main(address= your_address, geocoder_key= your_geocoder_key, nsdi_key= your_nsdi_key, code_key=your_code_key, bound= your_bound)
Mainpro.get_four_direction_coord()
Mainpro.get_four_direction_bbox()
Mainpro.get_four_direction_abnormal()
Mainpro.compare_four_direction()
Mainpro.draw_four_direction()




# rhino 파일로 제작하기



# plt.show()


# ref4에서 보다 싶이 국소적으로 유의미한 정보는 
# (도로명주소) (연속주제) (건물통합정보-마스터)에 한정됩니다.
# 연속주제는 그중에서 특수한 정보를 담고 있으므로 따로 특이구역 체크를 진행하며
# 도로명 주소와 건물 통합 정보-마스터에 있는 건물의 용도와 면적, 도로의 면적 등의 정보를 체크
# 주소지 근처에 특이 건물의 개수, 주거환경의 차이 등을 확인합니다.

# 88c6b251809f4831a79145d085e07ded