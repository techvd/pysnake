import logging
import json

from lib import splash
from lib import gameover
from lib import gamescene
from lib import layout
from lib import snake
from lib import textobject
from lib import food
from lib import wall
from lib import gui
from lib import background


class SceneLoader:
    def __init__(self, game):
        self.game = game
        self.event_manager = game.get_event_manager()
        self.scene = None

    def get_game(self):
        return self.game

    def get_scene(self):
        return self.scene

    def create_node(self, key, props):
        obj = None
        if key == 'layout':
            logging.debug("Loader: Creating layout...")
            obj = layout.Layout()
        elif key == 'background':
            logging.debug("Loader: Creating background...")
            obj = background.Background(self.game)
        elif key == 'food':
            logging.debug("Loader: Creating food...")
            obj = food.Food(self.game)
        elif key == 'snake':
            logging.debug("Loader: Creating snake...")
            obj = snake.Snake(self.game)
        elif key == 'wall':
            logging.debug("Loader: Creating wall...")
            obj = wall.Wall(self.game)
        elif key == 'panel':
            logging.debug("Loader: Creating gui panel...")
            obj = gui.GUIPanel(self.game)
        elif key == 'button':
            logging.debug("Loader Creating gui button...")
            obj = gui.GUIButton(self.game)
        elif key == 'text':
            logging.debug("Loader: Creating text...")
            obj = textobject.Text(self.game)
        if obj:
            obj.load_props(self, props)
            return obj
        else:
            logging.debug("Loader: unrecognized tag in create_node: ", key)
            return None

    def load_scene(self, file):
        with open(file) as level_file:
            logging.warning(f"Loader: Loading from {file}...")
            _level = json.load(level_file)
            # check type first
            _type = _level['type']
            self.scene = None
            if _type == 'splash':
                logging.debug("Loader: Creating splash scene...")
                self.scene = splash.SplashScene(self.game)
            elif _type == 'gameover':
                logging.debug("Loader: Creating gameover scene...")
                self.scene = gameover.GameOverScene(self.game)
            elif _type == 'game':
                logging.debug("Loader: Creating game scene...")
                self.scene = gamescene.GameScene(self.game)
            if self.scene is None:
                logging.debug("E: Cannot create scene from file")
                return None
            self.scene.load_props(self, _level)
            return self.scene
        return None
