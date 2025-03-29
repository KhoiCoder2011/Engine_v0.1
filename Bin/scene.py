from Model import *
from Setting import *
import threading
from numba import prange

render_dist = 128  # Khoảng cách render

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = [Chunk(self, chunk_size = 128)]
        self.camera = self.app.camera
        self.num_obj = len(self.objects)
        self.chunk_size = 16  # Kích thước mỗi chunk
        self.loaded_chunks = {}  # Lưu trữ các chunk đã tải

        #self.create_initial_chunks()

    def create_initial_chunks(self):
        camera_position = self.camera.position
        start_x = int(camera_position.x) // self.chunk_size * self.chunk_size
        start_z = int(camera_position.z) // self.chunk_size * self.chunk_size

        arr_x = prange(start_x - render_dist, start_x + render_dist + self.chunk_size, self.chunk_size)
        arr_z = prange(start_z - render_dist, start_z + render_dist + self.chunk_size, self.chunk_size)
        for x in arr_x:
            for z in arr_z:
                thread = threading.Thread(target=self.add_chunk((x, 0, z)))
                thread.start()
                thread.join()

    def add(self, model):
        self.objects.append(model)
    
    def remove(self, model):
        self.objects.remove(model)

    def render(self):
        for obj in self.objects:
            obj.render()

    def find_object(self, position):
        for obj in self.objects:
            if obj.position == position:
                return obj
        return None

    def add_chunk(self, position):
        if not self.find_object(position):
            chunk = Chunk(self, position=position)
            self.add(chunk)
            self.loaded_chunks[position] = chunk

    def remove_chunk(self, position):
        chunk = self.find_object(position)
        if chunk:
            self.remove(chunk)
            del self.loaded_chunks[position]

    def update(self):
        camera_position = self.camera.position

        min_x = int(camera_position.x) // self.chunk_size * self.chunk_size - render_dist
        max_x = int(camera_position.x) // self.chunk_size * self.chunk_size + render_dist
        min_z = int(camera_position.z) // self.chunk_size * self.chunk_size - render_dist
        max_z = int(camera_position.z) // self.chunk_size * self.chunk_size + render_dist

        for x in prange(min_x, max_x + self.chunk_size, self.chunk_size):
            for z in prange(min_z, max_z + self.chunk_size, self.chunk_size):
                if (x, 0, z) not in self.loaded_chunks:
                    thread = threading.Thread(target=self.add_chunk((x, 0, z)))
                    thread.start()
                    thread.join()

        chunks_to_remove = []
        for position in self.loaded_chunks:
            x, y, z = position
            if not (min_x <= x <= max_x and min_z <= z <= max_z):
                chunks_to_remove.append(position)

        for position in chunks_to_remove:
            self.remove_chunk(position)
