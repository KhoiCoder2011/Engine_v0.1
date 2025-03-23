import pygame as pg

pg.init()
pg.mixer.init()

class Audio:
    def __init__(self, path: str):
        self.path = path
        self.sound = pg.mixer.Sound(self.path)

    def play(self):
        self.sound.play()
