import logging
from lib import basescene


class SplashScene(basescene.BaseScene):
    def __init__(self, game):
        super().__init__(game)
        logging.debug("SPLASH Created!")
