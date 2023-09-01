import requests
import json

class CoordinateFromAddress:
    """
    주소를 같이 넣고 클래스를 정의하면 좌표를 리턴합니다.
    """

    def __init__(self, address: str, key: str):
        # type: (str, str) -> None

        self.address = address
        self.key = key
        self.get_coord()

    def get_coord (self):
        # type: () -> None
        """
        정의된 주소를 geocoorder를 통해 좌표를 리턴합니다. 
        """

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

class UsabilityCode:
    """
    클래스를 정의하면용도코드를 리턴합니다.
    """

    def __init__(self, key: str):
        # type: (str) -> None

        self.key = key
        self.code_list = self.get_coord()

    def get_coord (self):
        # type: () -> None
        """
        
        """

        apiurl = "https://apis.data.go.kr/1741000/StanBuildngUseCd/getStanBuildngUseCdList?serviceKey=" + self.key + "&numOfRows=1000&type=json"
        response = requests.get(apiurl)
        if response.status_code == 200:
            dictlist = json.loads(response.text)["StanBuildngUseCd"][1]["row"]   
            dict_key = {}
            for dict in dictlist:
                dict_key[dict["code_id"]] = dict["cd_nm"]
            return dict_key
        else:
            print ("님 인터넷 확인좀")

#shapely polygon to make whatever
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

class BBoxFromCoordinate:
    """
    바운딩 박스 클래스를 정의합니다. 사방점과, 호출을 위한 바운딩박스를 정의합니다.
    """

    def __init__(self, x:float, y:float, bound:int):
        # type: (float, float, int) -> None

        # 사방별로 기준점을 잡습니다.
        self.north = [x, y + bound]
        self.south = [x, y - bound]
        self.east = [x + bound, y]
        self.west = [x - bound, y]

        # 바운딩 면적을 정의합니다.
        self.area = (2 * bound) ** 2

        # 호출을 위한 바운딩 박스를 스트링으로 적어줍니다. 
        self.bbox = str(x + bound) + "," + str(y + bound) + "," + str(x - bound) + "," + str(y - bound)

    def get_seq_data(self, key: str):
        # type: (str) -> dict
        """
        시퀀스 데이터의 목록과 번호를 리턴합니다. 
        """

        url = 'http://www.nsdi.go.kr/lxportal/zcms/nsdi/platform/openapi.html?apitype=dataList&authkey=' + key
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.text
            return eval(json_data)
    
    def get_bbox_data(self, seq: str, key: str):
        # type: (str, str) -> None
        """
        들어온 시퀀스키에 맞춰 지오제이슨을 반환합니다. 
        """

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
            try:
                geojson = response.text
                return json.loads(geojson)
            except:
                print ("none")
        else:
            print('인터넷 확인 ㄱㄱ')

    def get_polygon_properties (self, geojson:dict):
        # type: (dict) -> list[dict]
        """
        들어온 지오 제이슨을 폴리곤화 및 제이슨에 들어있던 속성 리스트를 분리합니다. 
        """

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