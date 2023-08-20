#-*- encoding:utf-8 -*-
import requests as req
from Clients.BBox import BBox
from Clients.VWORLDClient import VWORLDClient
 
  
class NSDIClient:
  '''
  #TODO : ABSTRACTION
  '''
  
  #1 | CONSTANTS
  __NSDI_REQ_URL = 'http://www.nsdi.go.kr/lxportal/zcms/nsdi/platform/openapi.html?'
  __NSDI_API_KEY = '8f48d41ac7e24e6e87ccd39d0db8a186'
  __data_list = req.get(__NSDI_REQ_URL,params={
      'apitype' : 'dataList',
      'authkey' : __NSDI_API_KEY
    }).json()
  
  
  #2 | METHODS
    
  def show_data_list(self):
    [print(i) for i in self.__data_list]
    
  def get_column_list(self,obj_seq:str):
    return req.get(self.__NSDI_REQ_URL,params={
      'apitype' : 'columnList',
      'authkey' : self.__NSDI_API_KEY,
      'datasets' : obj_seq
    })
  
  def get_geoinfo(self,obj_seq:str,bbox:BBox):
    return req.get(self.__NSDI_REQ_URL,params={
      'apitype' : 'data',
      'resulttype' : 'geojson',
      'authkey' : self.__NSDI_API_KEY,
      'datasets' : obj_seq,
      'bbox' : bbox.__str__()
    }
  )