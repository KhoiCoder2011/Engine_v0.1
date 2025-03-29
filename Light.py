
from Model import *


class Light:
    def __init__(self, position=(10, 10, 10), color=(0.8, 0.8, 0.8)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.Ia = 0.59
        self.Is = 32.0
