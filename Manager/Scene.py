from Model import *
from Settings import *
from Manager import render_time, file

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.time = render_time.Time()
        self.time.start()
        file.Save([Cube(self.app, position = (x, y, z), texture_path='assets/mix.png', name=f'Cube ({x}, {y}, {z})') for x in range(7) for y in range(7) for z in range(7)], path = save_path).save()
        self.add(file.Load(self.app, save_path).load())
        
        self.time.end()
        self.rendering_time = self.time.get_time()
        self.num_obj = len(self.objects)

    def add(self, model):
        self.objects.append(model)
    
    def add(self, models : list):
        self.objects.extend(models)

    def remove(self, model):
        self.objects.remove(model)

    def render(self):
        for obj in self.objects:
            if obj.set_active:
                obj.render()

    def save(self):
        file.Save(self.objects, save_path).save()

    def update(self):...


