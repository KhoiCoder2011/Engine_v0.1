import configparser
import os
from lib.lib import mgl, glm

save_path = 'D:/info.json'
config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
icon_path = 'assets/icon.png'
engine_name = 'Modern Engine'

config = configparser.ConfigParser()
config.read(config_path)

if not config.sections():
    raise FileNotFoundError(f"Lỗi: Không tìm thấy hoặc không đọc được file cấu hình: {config_path}")

def get_config_value(section, option, value_type, default=None):
    """Lấy giá trị từ file config, trả về mặc định nếu không tìm thấy"""
    try:
        if value_type == int:
            return config.getint(section, option)
        elif value_type == float:
            return config.getfloat(section, option)
        elif value_type == bool:
            return config.getboolean(section, option)
        else:
            return config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        print(f"Cảnh báo: Không tìm thấy [{section}] {option}, dùng giá trị mặc định: {default}")
        return default

RES = glm.vec2(get_config_value('Window', 'res_x', int, 1280),
               get_config_value('Window', 'res_y', int, 720))

DISPLAY_RES = glm.vec2(get_config_value('Window', 'display_x', int, 1280),
                       get_config_value('Window', 'display_y', int, 720))

RENDER_MODE = mgl.TRIANGLES

WIDTH, HEIGHT = RES.x, RES.y
DISPLAY_WIDTH, DISPLAY_HEIGHT = DISPLAY_RES.x, DISPLAY_RES.y

RESOLUTION = (int(WIDTH), int(HEIGHT))
DISPLAY_RESOLUTION = (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))

SENSITIVITY = get_config_value('Camera', 'sensitivity', float, 0.1)
SPEED = get_config_value('Camera', 'speed', float, 2.5)

FOV = get_config_value('Camera', 'fov', float, 45.0)
ASPECT_RATIO = RES.x / RES.y
NEAR = get_config_value('Camera', 'near', float, 0.1)
FAR = get_config_value('Camera', 'far', float, 100.0)

BG_COLOR = glm.vec3(
    get_config_value('Window', 'r', float, 0.0),
    get_config_value('Window', 'g', float, 0.0),
    get_config_value('Window', 'b', float, 0.0)
)

IS_FPS_TEXT = get_config_value('Graphics', 'is_fps_text', bool, True)
IS_NUM_OBJ_TEXT = get_config_value('Graphics', 'is_num_obj_text', bool, True)

GL_MAJOR = get_config_value('Graphics', 'gl_major', int, 4)
GL_MINOR = get_config_value('Graphics', 'gl_minor', int, 5)