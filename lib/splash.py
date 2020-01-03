from lib import scene


class SplashScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game, None)
        self.name = "SPLASH"
        self.background = None

    def set_background(self, background):
        self.background = background
        self.add_object(self.background)

#    def draw(self):
#        # no need to clear screen
#        super().draw(self.screen)
