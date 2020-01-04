import pygame

from lib import gameobject
from lib import constants
from lib import utilities


class Text(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        _weight = 0
        self.anchor = ''
        self.font = None
        self.color = None
        self.text = ""

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        _weight = utilities.parse_value(props['weight'])
        self.anchor = props['anchor']
        self.font = pygame.font.Font(None, _weight)
        self.color = utilities.parse_color(props['color'])

    def set_text(self, text, adjust=False):
        self.text = text
        self.pygame_object = self.font.render(self.text, 1, self.color)
        self.bounds = self.pygame_object.get_rect()
        if adjust:
            self.adjust_layout()

    def adjust_layout(self):
        _pb = self.parent.get_bounds()
        print("PB: ", _pb)
        if self.anchor == "left":
            _x = _pb.left + 5 # just for spacing
            _y = _pb.top + (_pb.height - self.bounds.height) / 2
        if self.anchor == "right":
            _x = _pb.right - self.bounds.width - 5 # just for spacing
            _y = _pb.top + (_pb.height - self.bounds.height) / 2
        self.move_to(_x, _y)

    def draw(self, surface):
        #print("TEXT drawing ", self.text, " at ", self.position)
        super().draw(surface)
