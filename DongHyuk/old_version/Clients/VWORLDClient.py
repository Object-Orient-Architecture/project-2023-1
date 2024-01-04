import requests as req

class VWORLDClient:
  '''
  #TODO : ABSTRACTION
  '''
  
  #1 | CONSTANTS
  __VWORLD_DATA_URL = 'https://api.vworld.kr/req/data?'
  __VWORLD_GEO_URL = 'https://api.vworld.kr/req/address?'
  __VWORLD_API_KEY = '9BCCCEC1-2DCC-3043-B1BF-50B3D36B3102'
  
  #2 | METHODS
  def get_coords_from_address(self,address:str):
    response_json = req.get(self.__VWORLD_GEO_URL,params={
      'service' : 'address',
      'request' : 'getcoord',
      'version' : '2.0',
      'crs' : 'epsg:5179',
      'address' : address,
      'refine' : 'true',
      'simple' : 'false',
      'format' : 'json',
      'type' : 'road',
      'key' : self.__VWORLD_API_KEY
    }).json()
    
    if response_json['response']['status'] == 'ERROR':
      error_message = response_json['response']['error']['text']
      error_code = response_json['response']['error']['code']
      print(error_message)
      raise Exception(f'Vworld API Error : [{error_code}] {error_message}')
    else:
      x = response_json['response']['result']['point']['x']
      y = response_json['response']['result']['point']['y']
      return (float(x),float(y))
