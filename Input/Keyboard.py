from lib.lib import glfw

class Keyboard:
    def __init__(self, app):
        self.app = app
        self.window = self.app.window

    def is_click(self, click_key):
        if glfw.get_key(self.window, click_key) == glfw.PRESS:
            return True
        return False

