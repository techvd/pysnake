import pygame
from lib import utilities
from lib import constants


class GameObject:
    def __init__(self, game):
        self.name = "GAMEOBJECT"
        self.parent = None
        self.pygame_object = None
        self.game = game
        self.position = [0, 0]
        self.size = [0, 0]
        self.layer = 0
        self.bounds = None
        self.background_color = constants.BLACK
        self.background_image = None
        self.layout = None
        self.active = True
        self.visible = True
        self.collision = True
        self.frames = 0

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_position(self):
        return self.position

    def get_size(self):
        return self.size

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

    def is_collidible(self):
        return self.collision

    def set_collidible(self, collide):
        self.collision = collide

    def get_layer(self):
        return self.layer

    def set_layer(self, layer):
        self.layer = layer

    def load_props(self, scene_loader, props):
        if props is not None:
            if 'name' in props:
                self.name = props['name']
            if 'background_color' in props:
                self.background_color = utilities.parse_color(props['background_color'])
            if 'background' in props:
                self.background_image = scene_loader.create_node('background', props['background'])
            if 'position' in props:
                self.position = utilities.parse_2dvec(props['position'])
            if 'size' in props:
                self.size = utilities.parse_2dvec(props['size'])
            if 'layer' in props:
                self.layer = utilities.parse_value(props['layer'])
            if 'visible' in props:
                self.visible = utilities.parse_value(props['visible'])
            if 'layout' in props:
                self.layout = scene_loader.create_node('layout', props['layout'])
            self.update_bounds()

    def update_bounds(self):
        self.bounds = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def is_within(self, x, y):
        return self.bounds.collidepoint(x, y)

    def move_to(self, x, y):
        self.position[0] = x
        self.position[1] = y
        self.update_bounds()

    def update(self, dt):
        pass

    def draw(self, surface):
        if not self.visible:
            return
        if self.pygame_object:
            #print(self.pygame_object, self.bounds)
            surface.blit(self.pygame_object, self.bounds)
