import json
from Model import *
from Texture import *


class Save:
    def __init__(self, objects, path: str):
        self.objects = objects
        self.path = path

    def save(self):
        with open(self.path, 'w+') as file:
            json.dump([obj.to_dict() for obj in self.objects], file, indent=4)


class Load:
    def __init__(self, app, path: str):
        self.app = app
        self.path = path
        self.class_map = {
            "Cube": Cube
        }

    def load(self):
        obj = []
        with open(self.path, 'r') as file:
            file = json.load(file)
            for line in file:
                position = line['position']
                rotation = line['rotation']
                scale = line['scale']
                faces = line['faces']
                color = line['color']
                type = line['type']
                tag = line['tag']
                name = line['name']
                texture_path = line['texture_path']
                id = line['id']
                set_active = line['set_active']
                model = self.get_model(type, self.app, position, rotation, scale, faces, color, name, texture_path)
                model.tag = tag
                model.id = id
                model.set_active = set_active
                obj.append(model)
        return obj

    def get_model(self, type, *arg, **kwarg):
        return self.class_map[type](*arg, **kwarg)