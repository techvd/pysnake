import pygame
import json

from lib import scene
from lib import static


class GameOverScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game, None)
        self.name = "GAMEOVER"
        self.background = None
        self.load_scene('assets/gameover.json')

    def get_layout(self):
        return self.layout

    def load_scene(self, file):
        with open(file) as level_file:
            _level = json.load(level_file)
            self.name = _level['name']
            self.background = static.StaticObject(self.game, self, _level['background'])
            self.add_object(self.background)
            _button = _level['button']
            self.ok_btn = static.StaticObject(self.game, self, _button)
            self.add_object(self.ok_btn)

    def draw(self):
        # no need to clear screen
        super().draw(self.screen)
