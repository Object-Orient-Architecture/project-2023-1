import requests
import json

class CoordinateFromAddress:

    # 주소를 같이 넣고 클래스를 정의하면 좌표를 리턴합니다.
    def __init__(self, address: str, key: str):
        self.address = address
        self.key = key
        self.get_coord()

    
    # 정의된 주소를 geocoorder를 통해 좌표를 리턴합니다. 
    def get_coord (self):
        apiurl = "http://api.vworld.kr/req/address?"
        params = {
            "service": "address",
            "request": "getcoord",
            "crs": "epsg:5179",
            "address": self.address,
            "format": "json",
            "type": "road",
            "key": self.key
        }
        response = requests.get(apiurl, params=params)
        if response.status_code == 200:
            json_data = response.json()

            # 에러가 나면 에러난 이유를 호출합니다. 
            if (json_data['response']['status'] == "ERROR"):
                print (json_data['response']['error']['text'])
            else:
                # 에러가 안났다면 좌표를 self에 등록합니다.
                result = json_data['response']['result']['point']
                self.x = float(result["x"])
                self.y = float(result["y"])
        else:
            print ("님 인터넷 확인좀")

# test = CoordinateFromAddress("관천로 21", "27E280E5-0E68-3751-85C5-2802D1FA2BD1")


#shapely polygon to make whatever

from shapely.geometry import shape
from shapely.geometry.polygon import Polygon


# 바운딩 박스 클래스를 정의합니다.
class BBoxFromCoordinate:
    def __init__(self, x:float, y:float, bound:int):

        # 사방별로 기준점을 잡습니다. (아직 안씀)
        self.north = [x, y + bound]
        self.south = [x, y - bound]
        self.east = [x + bound, y]
        self.west = [x - bound, y]

        # 바운딩 면적을 정의합니다.
        self.area = (2 * bound) ** 2

        # 호출을 위한 바운딩 박스를 스트링으로 적어줍니다. 
        self.bbox = str(x + bound) + "," + str(y + bound) + "," + str(x - bound) + "," + str(y - bound)

    # 시퀀스 데이터의 목록과 번호를 리턴합니다. 
    def get_seq_data(self, key: str):
        url = 'http://www.nsdi.go.kr/lxportal/zcms/nsdi/platform/openapi.html?apitype=dataList&authkey=' + key
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.text
            return eval(json_data)
    
    # 들어온 시퀀스키에 맞춰 지오제이슨을 반환합니다. 
    def get_bbox_data(self, seq: str, key: str):
        url = (
            "https://www.nsdi.go.kr/lxportal/zcms/nsdi/platform/openapi.html?apitype=data&resulttype=geojson&datasets="
            + seq 
            + "&bbox=" 
            + self.bbox
            + "&authkey=" 
            + key
        )
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.text
            try:
                geojson = json.loads(json_data)
                return geojson
            except:
                print ("problem reading geojson")
        else:
            print('인터넷 확인 ㄱㄱ')

    # 들어온 지오 제이슨을 폴리곤화 및 제이슨에 들어있던 속성 리스트를 분리합니다. 
    def get_polygon_properties (self, geojson:dict):
        if (geojson):
            poly_list = []

            feature_list = geojson["features"]
            for feature in feature_list:
                temp_dict =  {}

                polygon: Polygon = shape( feature["geometry"])
                temp_dict["polygon"] = polygon
                temp_dict["properties"] = feature["properties"]
                poly_list.append(temp_dict)
                
            return poly_list
        
        
# bboxtest = BBoxFromCoordinate(test.x, test.y, 20)
# print(bboxtest.get_bbox_data(seq = "12623",key = "88c6b251809f4831a79145d085e07ded"))
# print(bboxtest.make_polygon())
# # 88c6b251809f4831a79145d085e07ded