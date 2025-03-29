import numpy as np
import math


class Cube_model:
    def __init__(self):
        self.vertices = np.array([
            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,

            -0.5, -0.5,  0.5,
            0.5, -0.5,  0.5,
            0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,

            -0.5, -0.5,  0.5,
            0.5, -0.5,  0.5,
            0.5, -0.5, -0.5,
            -0.5, -0.5, -0.5,

            -0.5,  0.5,  0.5,
            0.5,  0.5,  0.5,
            0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,

            -0.5, -0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,

            0.5, -0.5,  0.5,
            0.5,  0.5,  0.5,
            0.5,  0.5, -0.5,
            0.5, -0.5, -0.5
        ], dtype='f4')

        self.uv = np.array([
            0.0, 0.0,
            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,

            0.0, 0.0,
            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,

            0.5, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.5, 1.0,

            0.5, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.5, 1.0,

            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,
            0.0, 0.0,

            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,
            0.0, 0.0,
        ], dtype='f4')

        self.uv_none = np.array([0.0] * 48, dtype='i4')

        # Vector pháp tuyến cho mỗi mặt của cube (6 mặt)
        self.normals = np.array([
            # Mặt sau (z = 0.5)
            0.0, 0.0, 1.0,   # Pháp tuyến của mặt sau
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            # Mặt trước (z = -0.5)
            0.0, 0.0, -1.0,  # Pháp tuyến của mặt trước
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,

            # Mặt dưới (y = -0.5)
            0.0, -1.0, 0.0,  # Pháp tuyến của mặt dưới
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,

            # Mặt trên (y = 0.5)
            0.0, 1.0, 0.0,   # Pháp tuyến của mặt trên
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,

            # Mặt trái (x = -0.5)
            -1.0, 0.0, 0.0,  # Pháp tuyến của mặt trái
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,

            # Mặt phải (x = 0.5)
            1.0, 0.0, 0.0,   # Pháp tuyến của mặt phải
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0
        ], dtype='f4')


class Sphere_Model:
    def __init__(self, radius: int = 1, latitude_count: int = 100, longitude_count: int = 100):
        self.radius = radius
        self.latitude_count = latitude_count
        self.longitude_count = longitude_count
        self.vertices = np.zeros(
            (self.latitude_count + 1, self.longitude_count + 1, 3))
        self.uv = np.zeros(
            (self.latitude_count + 1, self.longitude_count + 1, 2))
        self.normals = np.zeros(
            (self.latitude_count + 1, self.longitude_count + 1, 3))
        self.indices = []
        self.generate_vertices()
        self.generate_indices()

    def generate_vertices(self):
        pi = math.pi
        for i in range(self.latitude_count + 1):
            phi = pi * i / self.latitude_count
            for j in range(self.longitude_count + 1):
                theta = 2.0 * pi * j / self.longitude_count

                x = self.radius * math.sin(phi) * math.cos(theta)
                y = self.radius * math.sin(phi) * math.sin(theta)
                z = self.radius * math.cos(phi)

                # u = theta / (2 * pi)
                # v = phi / pi

                self.vertices[i, j] = (x, y, z)
                # self.uv[i, j] = (u, v)

                length = math.sqrt(x**2 + y**2 + z**2)
                self.normals[i, j] = (x / length, y / length, z / length)

    def generate_indices(self):
        for i in range(self.latitude_count):
            for j in range(self.longitude_count):
                first = i * (self.longitude_count + 1) + j
                second = first + self.longitude_count + 1

                if i != 0:
                    self.indices.append((first, second, first + 1))
                if i != self.latitude_count - 1:
                    self.indices.append((first + 1, second, second + 1))


class Quad_Model:
    def __init__(self):
        self.vertices = np.array([
            -0.5, 0.0,  0.5,
            0.5, 0.0,  0.5,
            0.5, 0.0, -0.5,
            -0.5, 0.0, -0.5
        ], dtype='f4')

        self.uv = np.array([
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,
        ], dtype='f4')

        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype='u4')

        self.normal = np.array([
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0
        ])
