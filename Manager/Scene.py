from Model import *
from Setting import *
from Light import *
from Math.Math import Noise
from Manager import render_time, file
import random


class Scene:
    def __init__(self, app):
        self.app = app

        self.time = render_time.Time()
        self.time.start()
        self.light = self.app.light
        self.light_obj = Sphere(self.app, self.light.position, name = 'Directional Light', text_path='assets/mix.png')
        self.objects = [self.light_obj]
        self.noise = Noise()
        #file.Save(self.gen_model(), path=save_path).save()
        #self.add_model(file.Load(self.app, save_path).load())

        self.time.end()
        self.rendering_time = self.time.get_time()
        self.num_obj = len(self.objects)

    def gen_model(self, size_x: int = 25, size_z: int = 25):
        for x in range(size_x + 1):
            for z in range(size_z + 1):
                y = int(self.noise._sin_cos(x, z) * 2.15)
                yield Cube(self.app, position=(x, y, z), text_path='assets/mix.png')

    def add_model(self, model):
        self.objects.append(model)

    def add_model(self, models: list):
        self.objects.extend(models)

    def remove(self, model):
        self.objects.remove(model)

    def remove(self, models: list):
        self.objects = [obj for obj in self.objects if obj not in models]

    def render(self):
        for obj in self.objects:
            if obj.set_active and self.app.camera.is_point_in_frustum(self.app, obj.position):
                obj.render()

    def save(self):
        file.Save(self.objects, save_path).save()

    def update(self):
        self.light.position.y += 0.01
        self.objects[0].position = self.light.position
        self.objects.append(Cube(self.app, position = (random.randint(0, 25), random.randint(0, 25), random.randint(0, 25)), text_path='assets/mix.png'))
