# -*- coding:utf-8 -*-
try:
    from typing import List
except ImportError:
    pass

import rhino3dm as rh
from utils import explode

class WindowMaker:
    def __init__(self, boundary, floor, height):
        self.boundary = boundary
        self.floor = floor
        self.height = height

    def create(self):
        '''한 boundary에 대해 windows 생성'''
        # 모든 segments에 대해 windows 생성
        segments = explode(self.boundary)
        windows = []
        # 길이가 작은 segment 제외
        segments_selected = [segment for segment in segments if segment.Line.Length > 2.7]
        for segment in segments_selected:
            windows += self.create_window_on_segment(segment)
        return windows
        
    def create_window_on_segment(self, segment):
        '''한 segment에 대해 windows 생성'''

        def __divide_by_count(crv:rh.LineCurve,div_num:int)->List[float]:
            '''window 수만큼 나누기'''
            max_param = crv.Domain.T1
            result_params = []
            for i in range(div_num+1):
                result_params.append(i/div_num * max_param)
            return result_params

        def create_window_baselines(_segment):
            '''window가 그려질 baseline 생성'''
            # segment 길이 구하기
            segment_length = _segment.Line.Length
            
            # segment 분절
            dividing_number = int(segment_length//2.4)   # 분절된 길이의 최소 길이 2.4m. 즉, 창문 간 간격 최소 0.6m
            parameters = __divide_by_count(_segment,dividing_number)

            # 분절된 지점에 점 생성
            points = []
            for param in parameters:
                point = _segment.PointAt(param)
                points.append(point)
            
            # 이웃한 두 점씩 이어 분절된 선들 생성
            linecurves = []
            for i in range(len(points)-1):
                point = points[i]
                next_point = points[i+1]
                # line = geo.LineCurve(point, next_point)
                line = rh.LineCurve(point, next_point)
                linecurves.append(line)

            # window가 그려질 선들 생성
            windowcurves = []
            for linecurve in linecurves:
                # 분절된 선들의 중점 구하기
                mid_point = linecurve.Line.PointAt(0.5)
                # 중점을 기준으로 window가 그려질 선 생성
                tangent_start = linecurve.TangentAtStart
                tangent_start.X *= 0.9
                tangent_start.Y *= 0.9
                tangent_start.Z *= 0.9

                point1 = rh.Point3d(mid_point.X+tangent_start.X,mid_point.Y+tangent_start.Y, mid_point.Z+tangent_start.Z )
                point2 = rh.Point3d(mid_point.X-tangent_start.X,mid_point.Y-tangent_start.Y, mid_point.Z-tangent_start.Z )
                windowcurve = rh.LineCurve(point1, point2)
                windowcurves.append(windowcurve)
            return windowcurves

        def create_window_from_baseline(_windowcurve):
            '''windows 생성'''
            # 선을 extrude해 window 생성
            window = rh.Extrusion.Create(_windowcurve, 1.5, False)  # 높이 1.5m
            # window를 바닥면으로부터 높이기
            window.Translate(rh.Vector3d(0, 0, 1))   # 바닥면으로부터 1m
            # 각 층에 windows 생성
            print(f'height = {self.height} | floor = {self.floor}')
            res = [] 
            for j in range(self.floor):
                translated_window = window.Duplicate()
                translated_window.Translate(rh.Vector3d(0, 0, self.height*j))  # 한 층의 높이 4m
                res.append(translated_window)
            return res
            
        window_baselines = create_window_baselines(segment)
        # windows 생성
        translated_windows = []
        for windowcurve in window_baselines:
            translated_windows.extend(create_window_from_baseline(windowcurve))

        # windows 리턴
        return translated_windows