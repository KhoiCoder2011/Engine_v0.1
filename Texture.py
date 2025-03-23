import os
from lib.lib import pg, mgl

class Texture:
    def __init__(self, app, path: str):
        self.app = app
        self.ctx = app.ctx
        self.texture = self.load(path)

    def use(self, location: int = 0):
        self.texture.use(location=location)

    def load(self, path, flip_x=False, flip_y=True, anisotropy=32.0):
        abs_path = os.path.join(os.path.dirname(__file__), path)

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Lỗi: Không tìm thấy file texture tại {abs_path}")

        texture = pg.image.load(abs_path)
        texture = pg.transform.flip(texture, flip_x=flip_x, flip_y=flip_y)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=4,
            data=pg.image.tostring(texture, 'RGBA', False)
        )
        texture.anisotropy = anisotropy
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
