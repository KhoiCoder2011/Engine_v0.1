import os


class ShaderProgram:
    def __init__(self, app, shader_name='shader'):
        self.ctx = app.ctx

        base_path = os.path.join(os.path.dirname(__file__), 'shaders')
        vertex_shader_path = os.path.join(base_path, f'{shader_name}.vert')
        fragment_shader_path = os.path.join(base_path, f'{shader_name}.frag')

        if not os.path.exists(vertex_shader_path):
            raise FileNotFoundError(
                f"Lỗi: Không tìm thấy shader file {vertex_shader_path}")
        if not os.path.exists(fragment_shader_path):
            raise FileNotFoundError(
                f"Lỗi: Không tìm thấy shader file {fragment_shader_path}")

        with open(vertex_shader_path, 'r') as file:
            self.vertex_shader = file.read()

        with open(fragment_shader_path, 'r') as file:
            self.fragment_shader = file.read()

    def get_program(self):
        program = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_shader
        )
        return program
