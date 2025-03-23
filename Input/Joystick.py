from lib.lib import pg

class Joystick:
    def __init__(self):
        pg.joystick.init()
        self.joy_stick_count = pg.joystick.get_count()
        if self.joy_stick_count == 0:
            print("Không có Joystick kết nối!")
        else:
            print(f"Đã nhận {self.joy_stick_count}")
    
    def get_joystick(self, index : int):
        joystick = pg.joystick.Joystick(index)
        return joystick

    def event(self, joystick, event):
        x, y = 0, 0
        if event.type == pg.JOYAXISMOTION:
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            return (x, y)
