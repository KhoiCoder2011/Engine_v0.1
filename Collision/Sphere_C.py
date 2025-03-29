import glm

def is_collision(a : glm.vec3, b : glm.vec3, r_a, r_b):
    if glm.distance(a, b) >= r_a + r_b:
        return False
    return True
