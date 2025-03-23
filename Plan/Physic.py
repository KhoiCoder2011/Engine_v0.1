'''
a (m/s^2)
v (m/s)
t (s)
g (m/s^2)

GRAVITY = 9.81
acceleration = 0
velocity = 0
time = 0

'''

import glm
SCALE = 250
GRAVITY = -9.81 / SCALE


class Rigidbody:
    def __init__(self, object):
        self.objecxt = object
        self.position = object.position
        self.velocity = glm.vec3(0)
        self.is_gravity = True

    def update(self, time):
        if self.is_gravity:
            self.position += self.velocity
            self.velocity.y = round(GRAVITY * round(time, 3), 3)


class Ray:
    def __init__(self, origin: glm.vec3, target: glm.vec3):
        self.ox, self.oy, self.oz = origin
        self.tx, self.ty, self.tz = target

        self.dx = self.tx - self.ox
        self.dy = self.ty - self.oy
        self.dz = self.tz - self.oz

        length = glm.length(glm.vec3(self.dx, self.dy, self.dz))
        self.dx /= length
        self.dy /= length
        self.dz /= length

        self.diff = 1 / 10 ** 3

    def check_collision(self, point: glm.vec3, epsilon=0.001):

        x, y, z = self.ox, self.oy, self.oz
        while True:

            if glm.distance(glm.vec3(x, y, z), point) < epsilon:
                return True

            if glm.distance(glm.vec3(x, y, z), glm.vec3(self.tx, self.ty, self.tz)) < self.diff:
                break

            x += self.dx * self.diff
            y += self.dy * self.diff
            z += self.dz * self.diff

        return False


'''
ray = Ray(glm.vec3(0, 0, 0), glm.vec3(1, 1, 2))
print(ray.check_collision(glm.vec3(0.5, 0.5, 1)))
'''
