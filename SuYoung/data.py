# 필수 세팅
#-*- coding: utf-8 -*-

try:
    from typing import List, Tuple
except:
    ImportError

import math

import os
import Rhino.Geometry as rg     # type: ignore
import scriptcontext as sc      # type: ignore
import rhinoscriptsyntax as rs  # type: ignore
import Rhino.RhinoDoc as rd     # type: ignore
import Rhino.DocObjects as ro    # type: ignore

file_dir = rs.DocumentPath() + "SuYoung\\Data\\"
file_name = "furniture.3dm"

file_path = file_dir + file_name

def get_external_doc(path):
    # 경로를 설정하면 해당 파일을 RhinoDoc으로 반환하는 함수
    
    doc = rd.OpenHeadless(path)
    if doc:
        return doc    
    print("경로를 다시 확인해주세요.")

def find_obj_by_name(doc,name = str):
    # RhinoDoc과 이름을 입력하면 해당 DocObjects내의 동일한 이름을 가진 Object를 반환하는 함수
    if doc:
        
        objs = doc.Objects
        for obj in objs:
            
            if obj.Name == name :
                return obj
            
        print(name + "에 해당 하는 오브젝트가 없습니다.")
        return 0
            
    print("문서를 잘못 설정하였습니다.")

def get_geometry(object):
    # BrepObject를 입력하면 BrepGeometry를 반환하는 함수
    
    if (object):
        if(object.ObjectType == ro.ObjectType.Brep):
            return object.BrepGeometry
        
    print("가구가 없거나 Brep이 아닙니다.")
    return 0

def BrepfromFilebyName(file,type=str):
    # 파일과 오브젝트의 이름을 입력하면 해당 파일 내의 동일한 Name 속성을 가진 Brep오브젝트를 rg.Brep으로 반환하는 함수
    # file [path] -> str , type [name] -> str , Geometry -> rg.Brep
    
    doc = get_external_doc(file)
    object = find_obj_by_name(doc,type)
    return get_geometry(object)