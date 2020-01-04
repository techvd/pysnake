from lib import gameobject
from lib import utilities


class PhysicsObject(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.speed = 0

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.speed = utilities.parse_value(props['speed'])

    def update(self, dt):
        self.position[0] += self.speed[0] * dt
        self.position[1] += self.speed[1] * dt
        # print("New POS ", self.position)
