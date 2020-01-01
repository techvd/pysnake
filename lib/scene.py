import pygame

from lib import groupobject

class Scene(groupobject.GroupObject):
    def __init__(self, game, props):
        super().__init__(game, self, props)
        self.state = game.get_state()
        self.size = game.get_size()
        self.bounds = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.screen = game.get_screen()
        self.debug_counter = 0

    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

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
