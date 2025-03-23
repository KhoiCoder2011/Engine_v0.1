import imgui
from imgui.integrations.pygame import PygameRenderer
import pygame as pg
import moderngl as mgl
from Settings import config, config_path
from Manager.build import EngineBuilder


class CommandApp:
    def __init__(self, width=800, height=600):
        pg.init()
        self.width, self.height = width, height
        self.window = pg.display.set_mode(
            (width, height), flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption('Console')
        self.ctx = mgl.create_context()

        imgui.create_context()
        self.renderer = PygameRenderer()

        self.clock = pg.time.Clock()
        self.running = True

        self.input_buffer = ""
        self.command_history = []
        self.max_history = 1000
        self.enter_pressed = False
        self.scroll_to_bottom = False

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.enter_pressed = True

            self.renderer.process_event(event)

    def render_command_ui(self):
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.width, self.height)
        imgui.begin("Console")

        imgui.begin_child("ScrollingRegion", 0, 300, border=True,
                          flags=imgui.WINDOW_HORIZONTAL_SCROLLING_BAR | imgui.WINDOW_NO_RESIZE)

        for cmd in self.command_history:
            if isinstance(cmd, tuple):
                msg, color = cmd
                imgui.text_colored(msg, *color)
            else:
                imgui.text(cmd)

        if self.scroll_to_bottom:
            imgui.set_scroll_y(imgui.get_scroll_max_y())
            self.scroll_to_bottom = False

        imgui.end_child()

        imgui.text(">> ")
        imgui.same_line()

        imgui.set_keyboard_focus_here()

        _, self.input_buffer = imgui.input_text(
            "##cmd_input", self.input_buffer, 256, imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)

        if self.enter_pressed:
            self.execute_command(self.input_buffer)
            self.input_buffer = ""
            self.enter_pressed = False
            self.scroll_to_bottom = True

        imgui.end()

    def execute_command(self, command):
        if command.strip():
            self.command_history.append("> " + command)

            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)

            if command.lower() == 'exit()':
                self.running = False

            elif command.lower().startswith("set_res"):
                try:
                    _, resolution = command.split(" ", 1)
                    width, height = map(int, resolution.split('x'))

                    config['Window']['res_x'] = str(width)
                    config['Window']['res_y'] = str(height)
                    with open(config_path, 'w') as config_file:
                        config.write(config_file)

                    self.command_history.append(
                        (f"Resolution set to {width}x{height}",
                         (0.0, 1.0, 0.0, 1.0))
                    )

                except (ValueError, IndexError):
                    self.command_history.append(
                        ("Error: Invalid format! Use 'set_res widthxheight' (e.g., set_res 1280x720)",
                         (1.0, 0.0, 0.0, 1.0))
                    )
            elif command == 'build':
                builder = EngineBuilder()
                builder.run()
            elif command == "clear":
                self.command_history.clear()
            elif command == "help":
                self.command_history.append(
                    "Available commands: help, clear, exit, set_res [width]x[height], build")
            elif command == "exit":
                self.running = False
            else:
                self.command_history.append(
                    ("Unknown command: " + command, (1.0, 0.0, 0.0, 1.0)))

    def render(self):
        self.ctx.clear(0.1, 0.1, 0.1)

        imgui.new_frame()
        self.render_command_ui()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

        pg.display.flip()

    def run(self):
        imgui.get_io().display_size = (self.width, self.height)

        while self.running:
            self.process_events()
            self.render()
            self.clock.tick(60)

        self.cleanup()

    def cleanup(self):
        pg.quit()


if __name__ == "__main__":
    app = CommandApp()
    app.run()
