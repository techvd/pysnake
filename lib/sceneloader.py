import json

from lib import splash
from lib import gameover
from lib import gamescene
from lib import static
from lib import layout
from lib import snake
from lib import hud
from lib import textobject
from lib import food
from lib import gui
from lib import background


class SceneLoader:
    def __init__(self, game):
        self.game = game
        self.logger = game.get_logger()
        self.event_manager = game.get_event_manager()
        self.scene = None

    def get_game(self):
        return self.game

    def get_scene(self):
        return self.scene

    def create_node(self, key, node):
        obj = None
        if key == 'layout':
            self.logger.debug("Loader: Creating layout...")
            obj = layout.Layout()
        elif key == 'background':
            self.logger.debug("Loader: Creating background...")
            obj = background.Background(self.game)
        elif key == 'hud':
            self.logger.debug("Loader: Creating hud...")
            obj = hud.Hud(self.game)
        elif key == 'food':
            self.logger.debug("Loader: Creating food...")
            obj = food.Food(self.game)
        elif key == 'snake':
            self.logger.debug("Loader: Creating snake...")
            obj = snake.Snake(self.game)
        elif key == 'button':
            self.logger.debug("Loader Creating gui button...")
            obj = gui.GUIButton(self.game)
        elif key.startswith('text_'):
            self.logger.debug("Loader: Creating text...")
            obj = textobject.Text(self.game)
        if obj:
            obj.load_props(self, node)
            return obj
        else:
            self.logger.debug("Loader: unrecognized tag in create_node: ", key)
            return None

    def load_scene(self, file):
        with open(file) as level_file:
            self.logger.debug("Loader: Loading from ", file, "...")
            _level = json.load(level_file)
            # check type first
            _type = _level['type']
            self.scene = None
            if _type == 'splash':
                self.logger.debug("Loader: Creating splash scene...")
                self.scene = splash.SplashScene(self.game)
            elif _type == 'gameover':
                self.logger.debug("Loader: Creating gameover scene...")
                self.scene = gameover.GameOverScene(self.game)
            elif _type == 'game':
                self.logger.debug("Loader: Creating game scene...")
                self.scene = gamescene.GameScene(self.game)
            if self.scene is None:
                self.logger.debug("E: Cannot create scene from file")
                return None
            self.scene.load_props(self, _level)
            return self.scene
        return None
