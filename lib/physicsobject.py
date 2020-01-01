class PhysicsObject(GameObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        self.speed = parse_value(props['speed'])

    def update(self, dt):
        self.position[0] += self.speed[0] * dt
        self.position[1] += self.speed[1] * dt
        # print("New POS ", self.position)
