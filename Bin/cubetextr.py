import moderngl
import glfw
import numpy as np
from pyrr import Matrix44
from PIL import Image

if not glfw.init():
    raise Exception("GLFW can't be initialized")

window = glfw.create_window(800, 600, "3D Textured Cube", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)

ctx = moderngl.create_context()

ctx.enable(moderngl.DEPTH_TEST)

vertex_shader = """

in vec3 in_vert;
in vec2 in_text;
out vec2 v_text;
uniform mat4 mvp;
void main() {
    gl_Position = mvp * vec4(in_vert, 1.0);
    v_text = in_text;
}
"""


fragment_shader = """

in vec2 v_text;
out vec4 fragColor;
uniform sampler2D texture0;
void main() {
    fragColor = texture(texture0, v_text);
}
"""

prog = ctx.program(vertex_shader=vertex_shader,
                   fragment_shader=fragment_shader)

vertices = np.array([

    -0.5, -0.5,  0.5,  0.0, 0.0,
    0.5, -0.5,  0.5,  1.0, 0.0,
    0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,


    -0.5, -0.5, -0.5,  1.0, 0.0,
    0.5, -0.5, -0.5,  0.0, 0.0,
    0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,


    -0.5,  0.5, -0.5,  0.0, 1.0,
    0.5,  0.5, -0.5,  1.0, 1.0,
    0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,


    -0.5, -0.5, -0.5,  0.0, 0.0,
    0.5, -0.5, -0.5,  1.0, 0.0,
    0.5, -0.5,  0.5,  1.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 1.0,


    0.5, -0.5, -0.5,  1.0, 0.0,
    0.5,  0.5, -0.5,  1.0, 1.0,
    0.5,  0.5,  0.5,  0.0, 1.0,
    0.5, -0.5,  0.5,  0.0, 0.0,


    -0.5, -0.5, -0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5, -0.5,  0.5,  1.0, 0.0,
], dtype='f4')


indices = np.array([
    0, 1, 2,  2, 3, 0,
    4, 5, 6,  6, 7, 4,
    8, 9, 10, 10, 11, 8,
    12, 13, 14, 14, 15, 12,
    16, 17, 18, 18, 19, 16,
    20, 21, 22, 22, 23, 20,
], dtype='i4')


vbo = ctx.buffer(vertices)
ibo = ctx.buffer(indices)


vao = ctx.vertex_array(prog, [
    (vbo, '3f 2f', 'in_vert', 'in_text'),
], ibo)


texture_image = Image.open(
    "assets/grass.png").transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
texture = ctx.texture(texture_image.size, 3, texture_image.tobytes())
texture.build_mipmaps()


texture.use(location=0)


camera_pos = [3.0, 0.0, 3.0]
camera_target = [0.0, 0.0, 0.0]
camera_up = [0.0, 1.0, 0.0]


def mouse_callback(window, xpos, ypos):
    global camera_target
    width, height = glfw.get_window_size(window)
    x = (xpos / width - 0.5) * 2.0
    y = (ypos / height - 0.5) * 2.0
    camera_target = [x, -y, 0.0]


glfw.set_cursor_pos_callback(window, mouse_callback)


while not glfw.window_should_close(window):

    ctx.clear(0.1, 0.1, 0.1)

    model = Matrix44.identity()
    view = Matrix44.look_at(camera_pos, camera_target, camera_up)
    projection = Matrix44.perspective_projection(75.0, 800 / 600, 0.1, 100.0)
    mvp = projection * view * model

    prog['mvp'].write(mvp.astype('f4'))

    vao.render()

    glfw.swap_buffers(window)

    glfw.poll_events()


glfw.terminate()
