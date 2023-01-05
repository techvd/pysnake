from lib import staticobject


class Background(staticobject.StaticObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "BG"
