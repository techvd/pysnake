import pygame
import json

from lib import scene
from lib import static


class GameOverScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game)
        self.ok_btn = None

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'button' in props:
                ok_btn = scene_loader.create_node('button', props['button'])
                self.add_object(ok_btn)
