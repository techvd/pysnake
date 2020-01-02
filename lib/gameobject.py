import pygame
from lib import utilities


class GameObject:
    def __init__(self, game, scene, props=None):
        self.parent = None
        self.pygame_object = None
        self.game = game
        self.scene = scene
        self.position = [0, 0]
        self.size = [0, 0]
        self.bounds = None
        self.active = True
        self.visible = True
        self.load_props(props)

        self.frames = 0

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_position(self):
        return self.position

    def get_bounds(self):
        return self.bounds

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def is_visible(self):
        return self.visible

    def set_visible(self, vis):
        self.visible = vis

    def load_props(self, props):
        if props is not None:
            if 'position' in props:
                self.position = utilities.parse_2dvec(props['position'])
            if 'size' in props:
                self.size = utilities.parse_2dvec(props['size'])
            self.update_bounds()

    def update_bounds(self):
        self.bounds = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def move_to(self, x, y):
        self.position[0] = x
        self.position[1] = y
        self.update_bounds()

    def update(self, dt):
        pass

    def draw(self, surface):
        if self.pygame_object:
            surface.blit(self.pygame_object, self.bounds)