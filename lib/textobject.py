import logging
import pygame

from lib import gameobject
from lib import utilities


class Text(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "TEXT"
        self.anchor = None
        self.font = None
        self.color = None
        self.text = ""

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if 'anchor' in props:
            self.anchor = utilities.parse_2dvec(props['anchor'])
        _weight = utilities.parse_value(props['weight'])
        self.font = pygame.font.Font(None, _weight)
        self.color = utilities.parse_color(props['color'])

    def set_text(self, text, adjust=False):
        self.text = text
        self.pygame_object = self.font.render(self.text, 1, self.color)
        self.bounds = self.pygame_object.get_rect()
        # print(f"{self.name} SET {text},{adjust}")
        # self.dump()
        if adjust:
            self.adjust_layout()

    def adjust_layout(self):
        if self.anchor is not None:
            _x = self.anchor[0] - self.bounds.width / 2
            _y = self.anchor[1] - self.bounds.height / 2
            # print(f"{self.name} POST adjust")
            # self.dump()
            self.move_to(_x, _y)
