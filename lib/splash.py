import pygame
import json

from lib import scene
from lib import static


class SplashScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game, None)
        self.name = "SPLASH"
        self.background = None
        self.load_level('assets/splash01.json')

    def get_layout(self):
        return self.layout

    def load_level(self, file):
        with open(file) as level_file:
            _level = json.load(level_file)
            self.name = _level['name']
            self.background = static.StaticObject(self.game, self, _level['background'])
            self.add_object(self.background)

    def draw(self):
        # no need to clear screen
        super().draw(self.screen)
