from lib import static
from lib import utilities


class Food(static.StaticObject):
    def __init__(self, game):
        super().__init__(game)
        self.score = 0

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.score = utilities.parse_value(props['score'])

    def get_score(self):
        return self.score
