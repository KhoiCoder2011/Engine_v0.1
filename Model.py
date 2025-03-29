from Mesh import *
from Setting import *
from ObjLoader import *
from Terrain import *
from lib.lib import glm
from Texture import Texture
from Manager.Model import *
from Physic.RigidBody import Rigidbody

'''
f = Any number but != 0
faces = [f] * 6  
faces[0] -> faces[len(faces) - 1] = [Back, Front, Bottom, Top, Left, Right]
faces[0:5] = [Back, Front, Bottom, Top, Left, Right]

indices = [
    [0, 1, 2, 0, 2, 3],
    [4, 5, 6, 4, 6, 7],
    [8, 9, 10, 8, 10, 11],
    [12, 13, 14, 12, 14, 15],
    [16, 17, 18, 16, 18, 19],
    [20, 21, 22, 20, 22, 23]
]
'''


class BaseModel(Mesh):
    def __init__(self, o):
        self.app = o.app
        self.position = o.position
        self.rotation = o.rotation
        self.scale = o.scale
        self.faces = o.faces
        self.color = o.color
        self.name = o.name
        self.id = o.id
        self.tag = o.tag
        self.type = o.type
        self.vertices = o.vertices
        self.indices = o.indices
        self.normal = o.normal
        self.uv = o.uv
        self.set_active = o.set_active
        self.text_path = o.text_path
        self.rigidbody = o.rigidbody
        super().__init__(self)

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "scale": self.scale.to_tuple(),
            "faces": self.faces,
            "color": self.color,
            "text_path": self.text_path,
            "type": self.type,
            "tag": self.tag,
            "id": self.id,
            "set_active": self.set_active
        }


class Cube(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 faces: list = [1] * 6, color=(1, 1, 1), text_path: str = None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)

        self.text_path = text_path
        self.texture = Texture(app, text_path)
        self.set_active = True
        self.faces = faces

        self.tag = ''
        self.name = f'Cube {self.position.to_tuple()}'
        self.type = 'Cube'
        self.id = ''

        cube = Cube_model()
        self.vertices = cube.vertices
        self.uv = cube.uv
        self.normal = cube.normals
        self.indices = self.create_indices()

        self.color = color
        self.colors = [*color] * (len(self.vertices.tolist()) // 3)
        self.rigidbody = Rigidbody(self)
        super().__init__(self)

    def create_indices(self):
        face_indices = [
            [0, 1, 2, 0, 2, 3],
            [4, 5, 6, 4, 6, 7],
            [8, 9, 10, 8, 10, 11],
            [12, 13, 14, 12, 14, 15],
            [16, 17, 18, 16, 18, 19],
            [20, 21, 22, 20, 22, 23]
        ]

        indices = [idx for face, idx in zip(
            self.faces, face_indices) if face != 0]
        return np.array([index for sublist in indices for index in sublist], dtype='u4')


class Sphere(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), faces=None, color=(1, 1, 1), name='Sphere', text_path: str = None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)

        self.text_path = text_path
        self.texture = Texture(app, text_path)
        self.set_active = True
        self.faces = None

        self.tag = ''
        self.name = name
        self.type = 'Sphere'
        self.id = ''

        self.radius = 1
        self.latitude_count = 100
        self.longitude_count = 100

        sphere = Sphere_Model(
            self.radius, self.latitude_count, self.longitude_count)
        self.vertices, self.uv = sphere.vertices, sphere.uv

        self.normal = sphere.normals

        self.indices = sphere.indices
        self.color = color
        self.colors = [*color] * (len(self.vertices) // 3)
        self.rigidbody = Rigidbody(self)
        super().__init__(self)


class Quad(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), faces=None, color=(1, 1, 1), name='Quad', text_path: str = None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.color = color
        self.text_path = text_path
        self.texture = Texture(self.app, text_path)
        self.set_active = True
        self.faces = None

        self.tag = ''
        self.name = name
        self.type = 'Sphere'
        self.id = ''
        quad = Quad_Model()
        self.vertices, self.uv, self.normal, self.indices = quad.vertices, quad.uv, quad.normal, quad.indices
        self.colors = [*color] * (len(self.vertices.tolist()) // 3)
        self.rigidbody = Rigidbody(self)
        super().__init__(self)


class OBJModel(Mesh):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 faces=None, color=(1, 1, 1), name='OBJ', text_path: str = None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)

        self.text_path = text_path
        self.texture = Texture(app, text_path)
        self.set_active = True
        self.faces = faces

        self.tag = ''
        self.name = name
        self.type = 'OBJ'
        self.id = ''
        self.path = 'assets/meshes/axis.obj'

        objloader = get_info(self.path)
        self.vertices, self.normal, self.uv, self.indices = objloader

        self.f_color = color
        self.colors = [*color] * (len(self.vertices) // 3)
        self.rigidbody = Rigidbody(self)
        super().__init__(self)

    def update(self, time):
        self.rigidbody.update(time)

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "scale": self.scale.to_tuple(),
            "faces": self.faces,
            "color": self.f_color,
            "text_path": self.text_path,
            "type": self.type,
            "tag": self.tag,
            "id": self.id,
            "path": self.path,
            "set_active": self.set_active
        }
