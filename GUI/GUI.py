import glfw
import imgui
import glm
from imgui.integrations.glfw import GlfwRenderer


class GUI:
    def __init__(self, app):
        self.app = app

        self.window = app.window

        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        self.show_window = True
        self.scene = app.scene
        self.objects = self.scene.objects
        self.selected_object = None

    def quality_performance(self):
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(343, 100)
        imgui.begin("Performance", flags=imgui.WINDOW_NO_RESIZE)
        fps = self.app.fps
        if fps == 0:
            fps = 1
        imgui.text(f'FPS : {fps}')
        imgui.text((f'Ping : {1000 / fps :.3f} ms'))
        imgui.text(f"Objects: {len(self.objects)}")

        imgui.end()

    def object_manager(self):
        imgui.set_next_window_position(0, 100)
        imgui.set_next_window_size(343, 501)
        imgui.begin("Hierarchy", flags=imgui.WINDOW_NO_RESIZE)

        imgui.text(f"Game Object:")

        for obj in self.objects:
            is_selected = self.selected_object == obj
            clicked, _ = imgui.selectable(obj.name, is_selected)

            if clicked:
                self.selected_object = obj

        imgui.end()

    def inspector_window(self):
        imgui.set_next_window_position(1301, 0)
        imgui.set_next_window_size(349, 900)
        imgui.begin("Inspector", flags=imgui.WINDOW_NO_RESIZE)

        if self.selected_object:
            obj = self.selected_object
            set_active = obj.set_active
            model = obj.model

            imgui.text(f"Name : {obj.name}")

            imgui.text(f"Type : {obj.type}")

            changed, new_pos = imgui.input_float3("Position", *obj.position)
            if changed:
                obj.position = glm.vec3(*new_pos)

            changed, new_rot = imgui.input_float3("Rotation", *obj.rotation)
            if changed:
                obj.rotation = glm.vec3(*new_rot)

            changed, new_scale = imgui.input_float3("Scale", *obj.scale)
            if changed:
                obj.scale = glm.vec3(*new_scale)
            
            imgui.text(f'Velocity : {tuple(obj.rigidbody.velocity)}')

            changed, set_active = imgui.checkbox("Set active", set_active)
            if changed:
                obj.set_active = set_active

            changed, new_name = imgui.input_text("Name", obj.name, 256)
            if changed:
                obj.name = new_name

            changed, new_tag = imgui.input_text("Tag", obj.tag, 256)
            if changed:
                obj.tag = new_tag

            changed, new_id = imgui.input_text("ID", obj.id, 256)
            if changed:
                obj.id = new_id

            imgui.text('\n')
            imgui.text("Model:")
            imgui.text(self.matrix_to_string(model))
            imgui.text('\n')
            if imgui.button('Delete'):
                self.selected_object = None
                self.objects.remove(obj)

        imgui.end()

    def matrix_to_string(self, matrix):
        return "\n".join([f"{matrix[i][0]:.2f}\t{matrix[i][1]:.2f}\t{matrix[i][2]:.2f}\t{matrix[i][3]:.2f}" for i in range(4)])

    def render(self):
        self.impl.process_inputs()

        imgui.new_frame()

        if self.show_window:
            self.quality_performance()
            self.object_manager()
            self.inspector_window()

        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.draw()
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()
