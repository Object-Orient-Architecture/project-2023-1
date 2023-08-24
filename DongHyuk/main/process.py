from sma_app import SMA
from constants.options import BuildingType, VegetationType, ContourType, DetailType
from zipfile import ZipFile

sma_app = SMA()
sma_app.set_options(
  building_type=BuildingType.NATURAL,
  vegetation_type=VegetationType.POINT,
  detail_type=DetailType.MASS,
  contour_type=ContourType.CONTOUR
)

# file_path = 'DongHyuk\\main\\data_src\\376082597 - 아파트 + 역\\(B010)수치지도_376082597_2022_00000587663625.zip'
file_path = 'DongHyuk\\main\\data_src\\376120562 - 학교 + 산지\\(B010)수치지도_376120562_2022_00000642796721.zip'
file = ZipFile(file_path)
sma_app.set_file(file)
sma_app.operate()
sma_app.get_result()