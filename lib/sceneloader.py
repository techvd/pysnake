import pygame
import json

from lib import splash
from lib import gameover
from lib import gamescene
from lib import static
from lib import layout
from lib import utilities
from lib import snake
from lib import food
from lib import constants
from lib import hud


class SceneLoader:
    def load_scene(self, game, file):
        with open(file) as level_file:
            print("Loader: Loading from ", file, "...")
            _level = json.load(level_file)
            print(_level)
            # check type first
            _type = _level['type']
            _scene = None
            if _type == 'splash':
                print("Loader: Creating splash scene...")
                _scene = splash.SplashScene(game)
            elif _type == 'gameover':
                print("Loader: Creating gameover scene...")
                _scene = gameover.GameOverScene(game)
            elif _type == 'game':
                print("Loader: Creating game scene...")
                _scene = gamescene.GameScene(game)
            if _scene is None:
                print("E: Cannot create scene from file")
                return None
            for _key in _level:
                print("Loader: Processing ", _key, "...")
                if _key == 'name':
                    _scene.name = _level['name']
                    continue
                if _key == 'background':
                    print("Loader: Creating background...")
                    _background = static.StaticObject(game, _scene, _level['background'])
                    _scene.set_background(_background)
                    continue
                if _key == 'background_color':
                    print("Loader: Setting background color...")
                    _scene.set_background_color(utilities.parse_color(_level['background_color']))
                    continue
                if _key == 'layout':
                    # process layout
                    print("Loader: Creating layout...")
                    _layout = layout.Layout(_level['layout'])
                    _scene.set_layout(_layout)
                    continue
                if _key == 'hud':
                    # process hud
                    print("Loader: Creating hud...")
                    _hud = hud.Hud(game, _scene, _level['hud'])
                    _scene.add_hud(_hud)
                    continue
                if _key == 'snake':
                    print("Loader: Creating snake...")
                    _snake = snake.Snake(game, _scene, constants.YELLOW, _level['snake'])
                    _scene.add_snake(_snake)
                    continue
                if _key == 'food_items':
                    _food_nodes = _level['food_items']
                    print("Foods: #{}".format(len(_food_nodes)))
                    for node in _food_nodes:
                        _food = food.Food(game, _scene, node)
                        _scene.add_food(_food)
                    continue
                if _key == 'button':
                    _scene.add_button(_level['button'])
            return _scene
        return None
