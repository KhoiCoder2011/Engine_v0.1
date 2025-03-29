import glm
SCALE = 250
GRAVITY = -9.81 / SCALE


class Rigidbody:
    def __init__(self, object):
        self.objecxt = object
        self.position = object.position
        self.velocity = glm.vec3(0)
        self.accelation = glm.vec3(0)
        self.is_gravity = True

    def update(self, time):
        if self.is_gravity:
            self.position += self.velocity
            self.velocity.y = round(GRAVITY * round(time, 3), 3)