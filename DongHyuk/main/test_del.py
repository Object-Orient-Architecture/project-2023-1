import rhino3dm
import subprocess

# 메쉬 객체 생성
mesh = rhino3dm.Mesh()

# 메쉬 정점 추가
mesh.Vertices.Add(*(0, 0, 0))
mesh.Vertices.Add(*(1, 0, 0))
mesh.Vertices.Add(*(1, 1, 0))
mesh.Vertices.Add(*(0, 1, 0))

# 메쉬 면 추가
mesh.Faces.AddFace(0, 1, 2)
mesh.Faces.AddFace(0, 2, 3)



doc = rhino3dm.File3dm()
doc.Objects.AddMesh(mesh)
doc.Write('.\\test.3dm',version=6)
rhino_exe_path = r'C:\Program Files\Rhino 6\System\Rhino.exe'
file_to_open = '.\\test.3dm'
command = [rhino_exe_path, file_to_open]
subprocess.run(command)