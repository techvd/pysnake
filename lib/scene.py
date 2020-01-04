import pygame

from lib import groupobject


class Scene(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
        self.hud = None
        self.debug_counter = 0

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'hud' in props:
                self.hud = scene_loader.create_node('hud', props['hud'])
                self.add_object(self.hud)

    def end_scene(self):
        pass

    def do_fade(self, _from, _to):
        _incr = 8
        if _from > _to:
            _incr = -8
        _w = self.size[0]
        _h = self.size[1]
        print(_w, _h)
        _fade = pygame.Surface((_w, _h))
        _fade.fill((0, 0, 0))
        for alpha in range(_from, _to, _incr):
            _fade.set_alpha(alpha)
            self.draw()
            self.screen.blit(_fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)

    def fade_out(self):
        self.do_fade(0, 160)

    def fade_in(self):
        self.do_fade(160, 0)
