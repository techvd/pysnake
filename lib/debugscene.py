import pygame

from lib import constants
from lib import groupobject


class DebugScene(groupobject.GroupObject):
    def end_scene(self):
        pass

    def draw(self, surface, state):
        surface.fill(self.background_color, self.bounds)
        pygame.draw.line(surface, constants.WHITE, [0, 0], [200, 200], 5)
