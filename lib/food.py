from lib import static
from lib import utilities


class Food(static.StaticObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        self.score = utilities.parse_value(props['score'])

    def get_score(self):
        return self.score
