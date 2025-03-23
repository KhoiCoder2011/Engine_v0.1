from Mesh import *
from Settings import *
from ObjLoader import *
from Terrain import *
from lib.lib import glm
from numba import prange
from Texture import Texture
from Manager.model_info import *
from Plan.Physic import Rigidbody

'''

f = Any character but != None
faces = [f] * 6  
faces[0] -> faces[len(faces) - 1] = [Back, Front, Bottom, Top, Left, Right]
faces[0:5] = [Back, Front, Bottom, Top, Left, Right]

cube_vertices = [
    [0, 1, 2, 0, 2, 3],
    [4, 5, 6, 4, 6, 7],
    [8, 9, 10, 8, 10, 11],
    [12, 13, 14, 12, 14, 15],
    [16, 17, 18, 16, 18, 19],
    [20, 21, 22, 20, 22, 23]
]

'''


class OBJTM(Mesh):
    def __init__(self, app, objects, texture):
        self.app = app
        self.objects = objects
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)
        self.texture = texture
        self.text_coord = [objects[0].text_coord] * len(objects)

        self.vertices, self.indices, self.color = self.create_vertices()

        super().__init__(self)

    def create_indices(self, faces):
        face_indices = [
            [4, 5, 6, 6, 7, 4],
            [0, 1, 2, 2, 3, 0],
            [0, 1, 5, 5, 4, 0],
            [3, 2, 6, 6, 7, 3],
            [0, 3, 7, 7, 4, 0],
            [1, 2, 6, 6, 5, 1]
        ]

        indices = [idx for face, idx in zip(
            faces, face_indices) if face is not None]
        return [index for sublist in indices for index in sublist]

    def create_vertices(self, size=1):
        vertices = []
        indices = []
        color = []
        offset = 0

        s = size / 2
        for object in self.objects:
            x, y, z = object.position.x, object.position.y, object.position.z

            cube_vertices = [
                x - s, y - s, z + s,
                x + s, y - s, z + s,
                x + s, y + s, z + s,
                x - s, y + s, z + s,
                x - s, y - s, z - s,
                x + s, y - s, z - s,
                x + s, y + s, z - s,
                x - s, y + s, z - s
            ]

            vertices.extend(cube_vertices)

            cube_indices = self.create_indices(object.faces)

            indices.extend([i + offset for i in cube_indices])
            color.extend(object.color)
            offset += 8

        return vertices, indices, color


class Cube(Mesh):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 faces: list = [1] * 6, color=(1, 1, 1), name = 'Cube', texture_path : str = None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)

        self.texture_path = texture_path
        self.texture = Texture(app, texture_path)
        self.set_active = True
        self.faces = faces

        self.tag = ''
        self.name = name
        self.type = 'Cube'
        self.id = ''

        cube_model = Cube_model()
        self.vertices, self.text_coord = cube_model.vertices, cube_model.text_coord

        '''self.normal = np.array([
            *[ 0.0,  0.0,  1.0] * 4,
            *[ 0.0,  0.0, -1.0] * 4,
            *[ 0.0,  1.0,  1.0] * 4,
            *[ 0.0, -1.0,  0.0] * 4,
            *[ 1.0,  0.0,  0.0] * 4,
            *[-1.0,  0.0,  0.0] * 4,
        ], dtype = 'f4')'''

        self.indices = self.create_indices()
        self.f_color = color
        self.color = [*color] * (len(self.vertices.tolist()) // 3)
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
            "texture_path" : self.texture_path,
            "type": 'Cube',
            "tag": self.tag,
            "id": self.id,
            "set_active" : self.set_active
        }

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


class Quad(Mesh):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), color=(1, 1, 1), faces: list = [0] * 6, texture=None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.color = color
        self.texture = texture
        self.faces = faces

        self.vertices = np.array([
            -0.5, 0.0,  0.5,
            0.5, 0.0,  0.5,
            0.5, 0.0, -0.5,
            -0.5, 0.0, -0.5
        ], dtype='f4')

        self.text_coord = np.array([
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,
        ], dtype='f4')

        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype='u4')
        self.color = [*color] * (len(self.vertices.tolist()) // 3)
        super().__init__(self)


class ObjModel(Mesh):
    def __init__(self, app, path, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), color=(1, 1, 1), texture=None):
        self.app = app
        self.path = path
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.obj_loader = ObjLoader(self.path)
        self.texture = texture

        self.vertices = self.obj_loader.get_vertices()
        self.indices = self.obj_loader.get_indices()
        self.normals = self.obj_loader.get_normals()
        self.text_coord = self.obj_loader.get_texture_coords()
        self.color = [color] * len(self.vertices)

        super().__init__(self)


class Chunk:
    def __init__(self, app, chunk_size: int = 16, cave_depth: int = 10):
        self.app = app
        self.chunk_size = chunk_size
        self.cave_depth = cave_depth
        self.gen_chunk()
        self.chunk = OBJTM(self.app, self.voxels,
                           texture=Texture(self.app, 'assets/mix.png'))

    def gen_voxel(self):
        arr = prange(self.chunk_size + 1)
        voxels = []

        for x in arr:
            for z in arr:
                pos = glm.vec3(x, int(sin_cos(x, z) * 3.5), z)
                voxels.append(pos)
        return voxels

    def hash31(self, num: int):
        p3 = glm.fract(glm.vec3(num) * glm.vec3(0.1031, 0.1030, 0.0973))
        p3 += glm.dot(p3, p3.yzx + 33.33)
        return glm.fract((p3.xxy + p3.yzz) * p3.zyx)

    def gen_chunk(self):
        self.voxels = []
        voxels = self.gen_voxel()

        directions = [
            glm.vec3(0,  0, -1),
            glm.vec3(0,  0,  1),
            glm.vec3(0, -1,  0),
            glm.vec3(0,  1,  0),
            glm.vec3(-1,  0,  0),
            glm.vec3(1,  0,  0)
        ]

        voxel_set = set(tuple(v) for v in voxels)

        for position in voxels:
            faces = [None] * 6

            for i, direction in enumerate(directions):
                if tuple(position + direction) not in voxel_set:
                    faces[i] = 1

            if faces != [0] * 6:
                color = self.hash31(position.x + position.y + position.z)
                cube = Cube(self.app, position, faces=faces)
                self.voxels.append(cube)

    def render(self):
        self.chunk.render()


class BigChunk:
    def __init__(self, app, chunk_size: int = 16):
        self.app = app
        self.chunk_size = chunk_size
        self.gen_chunk()
        self.chunk = OBJTM(self.app, self.voxels)

    def gen_voxel(self):
        arr = prange(self.chunk_size + 1)
        for x in arr:
            for y in arr:
                for z in arr:
                    yield glm.vec3(x, y, z)

    def hash31(self, num: int):
        p3 = glm.fract(glm.vec3(num) * glm.vec3(0.1031, 0.1030, 0.0973))
        p3 += glm.dot(p3, p3.yzx + 33.33)
        return glm.fract((p3.xxy + p3.yzz) * p3.zyx)

    def gen_chunk(self):
        self.voxels = []
        voxels = self.gen_voxel()

        directions = np.array([
            glm.vec3(0,  0, -1),
            glm.vec3(0,  0,  1),
            glm.vec3(0, -1,  0),
            glm.vec3(0,  1,  0),
            glm.vec3(-1,  0,  0),
            glm.vec3(1,  0,  0)
        ])

        for position in voxels:
            faces = [None] * 6

            for i, direction in enumerate(directions):
                if position + direction not in voxels:
                    faces[i] = 0

            if faces != [None] * 6:
                color = self.hash31(position.x + position.y + position.z)
                self.voxels.append(
                    Cube(self.app, position, faces=faces, color=color))

    def render(self):
        self.chunk.render()


class BasicChunk:
    def __init__(self, app, scene, chunk_size: int = 16, cave_depth: int = 5):
        self.app = app
        self.scene = scene
        self.chunk_size = chunk_size
        self.cave_depth = cave_depth
        self.initalize()
        self.position = glm.vec3(0)
        self.scene.objects.extend(self.voxels)

    def gen_voxel(self):
        v = []
        arr = prange(self.chunk_size + 1)
        for x in arr:
            for z in arr:
                p = glm.vec3(x, int(sin_cos(x, z) * 2), z)
                v.append(p)
                _from = int(p.y - 1)
                _to = -self.cave_depth
                for y in range(_to, _from, 1):
                    p = glm.vec3(p.x, y, p.z)
                    v.append(p)
        return v

    def initalize(self):
        self.voxels = []
        voxels = self.gen_voxel()
        num_voxels = len(voxels)
        texture = Texture(self.app, 'assets/mix.png')

        directions = np.array([
            glm.vec3(0,  0, -1),
            glm.vec3(0,  0,  1),
            glm.vec3(0, -1,  0),
            glm.vec3(0,  1,  0),
            glm.vec3(-1,  0,  0),
            glm.vec3(1,  0,  0)
        ])

        for position in voxels:
            faces = [None] * 6

            for i, direction in enumerate(directions):
                if position + direction not in voxels:
                    faces[i] = 0

            if faces != [None] * 6:
                print(f'{len(self.voxels) / num_voxels * 100 :.3f} %')
                self.voxels.append(
                    Cube(self.app, position, faces=faces, texture=texture))
            else:
                num_voxels -= 1

    def render(self):
        pass
