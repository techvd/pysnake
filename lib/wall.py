import pygame

from lib import gameobject
from lib import constants
from lib import utilities


class Wall(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "WALL"
        self.color = constants.WHITE

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.color = utilities.parse_color(props['color'])

    def draw(self, surface, state):
        pygame.draw.rect(surface, self.color, self.bounds)
