from lib import tilescene


class SplashScene(tilescene.TileScene):
    def __init__(self, game):
        super().__init__(game)
        self.logger.debug("SPLASH Created!")
