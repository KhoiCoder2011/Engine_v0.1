import trimesh
import numpy as np


def get_info(path: str):
    mesh = trimesh.load_mesh(path)

    vertices = np.array(mesh.vertices, dtype='f4')
    face_normals = np.array(mesh.face_normals, dtype='f4')
    faces = np.array(mesh.faces, dtype='i4')

    if hasattr(mesh.visual, 'uv') and mesh.visual.uv is not None:
        uv = np.array(mesh.visual.uv, dtype='f4')
    else:

        uv = np.zeros((len(vertices), 2), dtype='f4')

    return vertices, face_normals, uv, faces
