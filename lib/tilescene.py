from lib import groupobject


class TileScene(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
        self.hud = None
        self.debug_counter = 0
        self.htile_size = 40
        self.vtile_size = 40
        self.htiles = 18
        self.vtiles = 32

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'hud' in props:
                self.hud = scene_loader.create_node('hud', props['hud'])
                self.add_child(self.hud)

    def end_scene(self):
        pass
