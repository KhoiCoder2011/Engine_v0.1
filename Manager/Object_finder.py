from lib.lib import glm


class Find_OBJ:
    def __init__(self, scene):
        self.objects = scene.objects

    def find_tag(self, tag: str):
        objs = []
        for obj in self.objects:
            if obj.tag == tag:
                objs.append(obj)
        return objs

    def find_position(self, position: glm.vec3):
        for obj in self.objects:
            if obj.position == position:
                return obj
        return None

    def find_name(self, name: str):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def find_id(self, id : str):
        for obj in self.objects:
            if obj.id == id:
                return obj
        return None
