import requests

# "compute_rhino3d" API 엔드포인트
compute_url = "https://compute.rhino3d.com"

# 입력 점 데이터
input_points = [
    {"X": 0, "Y": 0, "Z": 0},
    {"X": 5, "Y": 10, "Z": 0},
    {"X": 10, "Y": 0, "Z": 0},
    # ... 추가적인 점 데이터
]

# Delaunay 삼각화를 위한 입력 데이터 구성
input_data = {
    "points": input_points
}

# "compute_rhino3d" API 호출
response = requests.post(compute_url + "/v1/delaunay", json=input_data)

if response.status_code == 200:
    result = response.json()
    # 삼각화된 메시를 얻습니다.
    mesh = result["mesh"]
    print("Delaunay 삼각화 결과:", mesh)
else:
    print("API 호출 실패:", response.text)
