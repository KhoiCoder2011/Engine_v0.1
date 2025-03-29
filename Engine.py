from Delete_cache import *
from Setting import *
from GUI.GUI import *
from lib.lib import mgl
from Input.Keyboard import Keyboard
from Shader import ShaderProgram
from Manager.Scene import Scene
from Manager.Audio import *
from Camera import Camera
from Light import Light
import sys
import glfw
sys.path.append('D:/Dev/Python/Modern_GL/Engine_GLFW/source')

class Engine:
    def __init__(self):
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.window = glfw.create_window(
            *RESOLUTION, f"Modern Engine | OpenGL {GL_MAJOR}.{GL_MINOR}", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")
        
        glfw.set_window_pos(self.window, 15, 30)
        glfw.make_context_current(self.window)
        #glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.ctx = mgl.create_context()
        #self.ctx.viewport = (343, HEIGHT - 501, 958, 501)

        self.ctx.multisample = False
        self.ctx.enable(mgl.DEPTH_TEST | mgl.BLEND)
        self.ctx.gc_mode = 'auto'
        self.delta_time = 0
        self.time = 0
        self.last_time = glfw.get_time()
        self.fps = 0
        self.last_x, self.last_y = RESOLUTION
        self.on_init()

    def on_init(self):
        self.camera = Camera()
        self.shader = ShaderProgram(self)
        self.prog = self.shader.get_program()
        self.light = Light()
        self.scene = Scene(self)
        self.keyboard = Keyboard(self)
        self.gui = GUI(self)

    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        self.gui.render()

    def update(self):
        self.camera.update_view_matrix()
        current_time = glfw.get_time()
        self.delta_time = current_time - self.last_time
        self.time += self.delta_time
        self.fps = round(1 / self.delta_time, 3)
        self.last_time = current_time
        self.scene.update()

    def destroy(self):
        self.ctx.release()
        self.prog.release()
        delete_pycache(".")

    def handle_events(self):
        if self.keyboard.is_click(glfw.KEY_W):
            self.camera.process_keyboard('FORWARD', self.delta_time)
        if self.keyboard.is_click(glfw.KEY_S):
            self.camera.process_keyboard('BACKWARD', self.delta_time)
        if self.keyboard.is_click(glfw.KEY_A):
            self.camera.process_keyboard('LEFT', self.delta_time)
        if self.keyboard.is_click(glfw.KEY_D):
            self.camera.process_keyboard('RIGHT', self.delta_time)
        if self.keyboard.is_click(glfw.KEY_E):
            self.camera.process_keyboard('UP', self.delta_time)
        if self.keyboard.is_click(glfw.KEY_Q):
            self.camera.process_keyboard('DOWN', self.delta_time)

        glfw.poll_events()

        if glfw.window_should_close(self.window) or self.keyboard.is_click(glfw.KEY_ESCAPE):
            self.destroy()
            self.scene.save()
            glfw.terminate()
            sys.exit()

        mouse_x, mouse_y = glfw.get_cursor_pos(self.window)
        xoffset = mouse_x - self.last_x
        yoffset = self.last_y - mouse_y
        self.camera.process_mouse_movement(xoffset, yoffset)
        self.last_x, self.last_y = mouse_x, mouse_y

    def run(self):
        while not glfw.window_should_close(self.window):
            self.handle_events()
            self.update()
            self.render()
            glfw.swap_buffers(self.window)

        glfw.terminate()

e = Engine()
e.run()