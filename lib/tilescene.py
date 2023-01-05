from lib import basescene
from lib import utilities


class TileScene(basescene.BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.htile_size = 40
        self.vtile_size = 40
        self.htiles = 32
        self.vtiles = 18

    def inject_props(self, node):
        # pos in tiles
        pos = utilities.parse_2dvec(node['position'])
        node['position'] = [pos[0] * self.htile_size, pos[1] * self.vtile_size]
        # size in tiles
        if 'size' in node:
            size = utilities.parse_2dvec(node['size'])
            node['size'] = [size[0] * self.htile_size, size[1] * self.vtile_size]
        else:
            node['size'] = [self.htile_size, self.vtile_size]

    def create_object(self, scene_loader, props, key):
        self.inject_props(props)
        return super().create_object(scene_loader, props, key)
