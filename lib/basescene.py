import logging
import pygame
from lib import groupobject


class BaseScene(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "SCENE"
        self.paused = False
        self.debug_counter = 0

    def end_scene(self):
        pass

    def set_background_color(self, col):
        self.background_color = col

    def get_layout(self):
        return self.layout

    def set_layout(self, layout):
        self.layout = layout
        self.bounds = pygame.Rect(layout.border_left, layout.border_top,
                                  self.size[0] - layout.border_right,
                                  self.size[1] - layout.border_bottom)

    def create_object(self, scene_loader, node, key):
        return scene_loader.create_node(key, node)

    def pause(self):
        logging.debug("Pausing scene")
        self.paused = True
        self.ignore_events = True

    def resume(self):
        logging.debug("Resuming scene")
        self.paused = False
        self.ignore_events = False
