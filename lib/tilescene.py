import pygame
from lib import basescene
from lib import utilities


class TileScene(basescene.BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.name = "TILESCENE"
        # defaults for 720x1280
        self.tile_size = [40, 40]
        self.tiles = [32, 18]

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.tile_size = utilities.parse_2dvec(props['tile_size'])
        self.tiles = utilities.parse_2dvec(props['tiles'])

    def inject_props(self, node):
        # pos in tiles
        pos = utilities.parse_2dvec(node['position'])
        node['tile_position'] = pos # preserve if needed
        node['position'] = [pos[0] * self.tile_size[0], pos[1] * self.tile_size[1]]
        # size in tiles
        if 'size' in node:
            size = utilities.parse_2dvec(node['size'])
            node['size'] = [size[0] * self.tile_size[0], size[1] * self.tile_size[1]]
        else:
            node['size'] = self.tile_size

    def create_object(self, scene_loader, props, key):
        self.inject_props(props)
        return super().create_object(scene_loader, props, key)

    def get_tile_bounds(self, x, y):
        tx = x * self.tile_size[0]
        ty = y * self.tile_size[1]
        return pygame.Rect(tx, ty, self.tile_size[0], self.tile_size[1])
