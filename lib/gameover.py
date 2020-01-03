import pygame
import json

from lib import scene
from lib import static


class GameOverScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game, None)
        self.name = "GAMEOVER"
        self.background = None
        self.ok_btn = None

    def set_background(self, background):
        self.background = background
        self.add_object(self.background)

    def add_button(self, button):
        self.ok_btn = static.StaticObject(self.game, self, button)
        self.add_object(self.ok_btn)
