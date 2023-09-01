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
your_bound = 350

class AbnormalFinder:
    """
    좌표를 넣어주면 사방의 비교를 해주는 함수입니다
    """

    def __init__(self, address: str, geocoder_key: str, nsdi_key: str, code_key: str, bound: int):
        # type: (str, str, str, str, int) -> None

        self.address = address 
        self.geocode_key = geocoder_key
        self.nsdi_key = nsdi_key
        self.code_key = code_key
        self.bound = bound
    
    def get_four_direction_list (self):
        # type: () -> None
        """
        주소를 토대로 사방의 흥미로운 지점들을 찾습니다.
        """
        
        # 주소로 부터 좌표를 찾습니다.
        self.coordinate_centre = addr.CoordinateFromAddress(self.address, self.geocode_key)
        # 찾은 좌표를 바운딩 박스로 제작합니다.
        self.bbox_centre = addr.BBoxFromCoordinate(self.coordinate_centre.x, self.coordinate_centre.y, self.bound)

        self.four_direction_coord = [
            self.bbox_centre.east, 
            self.bbox_centre.west, 
            self.bbox_centre.north,
            self.bbox_centre.south
        ]

        self.four_direction_bbox = [
            addr.BBoxFromCoordinate(coord[0],coord[1], self.bound) 
            for coord in self.four_direction_coord
        ]
        self.seqjson_centre = self.bbox_centre.get_seq_data(key = self.nsdi_key)

        self.four_direction_abnormal = [
            check.AbnormalCheck(
                seq_json=self.seqjson_centre, 
                bbox=bbox,
                nsdi_key=self.nsdi_key, 
                code_key=self.code_key
            )
            for bbox in self.four_direction_bbox
        ]

        self.usability_list = []
        self.interests_list = []

        for abnormal in self.four_direction_abnormal:
            try:
                usability = abnormal.use_dict
            except:
                usability = False
            interests = abnormal.interest_list

        
            if usability:
                self.usability_list.append(usability)
            self.interests_list.append(interests)

    
    def compare_four_direction(self):
        # type: () -> None
        """
        전단계의 결과를 토대로 사방의 흥미로운 지점들을 비교합니다.
        """

        self.dictcomp = cp.DictionaryComparison(self.usability_list)
        self.interecomp = cp.InterestsComparison(self.interests_list)

    def draw_four_direction(self):
        # type: () -> None
        """
        비교 결과를 라이노로 나타냅니다.
        """
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

process = AbnormalFinder(
    address= your_address, 
    geocoder_key= your_geocoder_key, 
    nsdi_key= your_nsdi_key, 
    code_key=your_code_key, 
    bound= your_bound
)
process.get_four_direction_list()
process.compare_four_direction()
process.draw_four_direction()