import pygame
from functools import partial

from lib import scene
from lib import utilities
from lib import eventmanager


class GameScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game)
        self.snake = None
        self.food_objects = []
        # self.debug = Text(self, "PySnake")
        # self.game_objects.append(self.debug)

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'snake' in props:
                snake_obj = scene_loader.create_node('snake', props['snake'])
                self.setupPlayer(snake_obj)
            if 'food_items' in props:
                _food_nodes = props['food_items']
                self.logger.debug("Foods: #{}".format(len(_food_nodes)))
                for node in _food_nodes:
                    food_obj = scene_loader.create_node('food', node)
                    self.add_food(food_obj)

    def set_background_color(self, col):
        self.background_color = col

    def get_layout(self):
        return self.layout

    def set_layout(self, layout):
        self.layout = layout
        self.bounds = pygame.Rect(layout.border_left, layout.border_top,
                                  self.size[0] - layout.border_right,
                                  self.size[1] - layout.border_bottom)

    def add_hud(self, hud):
        # TODO assume just one for now
        self.hud = hud
        self.add_child(self.hud)

    def add_snake(self, snake):
        self.snake = snake
        self.setupPlayer(snake)

    def add_food(self, food):
        self.food_objects.append(food)
        self.add_child(food)

    def setupPlayer(self, snake):
        self.snake = snake
        self.add_child(self.snake)
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_POSITION_CHANGED, self)
        self.ignore_events = False

    def resetPlayer(self):
        self.snake.reset()
        self.ignore_events = False
        self.snake.set_active(True)
        # what else to do here?

    def onGameOver(self):
        self.ignore_events = True
        self.snake.set_active(False)
        self.logger.debug("GAME OVER!!!")
        self.event_manager.raise_event(eventmanager.GAMEEVENT_GAME_OVER)

    def handleDeath(self):
        self.logger.debug("Player is DEAD!")
        self.game.get_state().update_lives(-1)
        if self.game.get_state().lives > 0:
            self.ignore_events = True
            self.snake.set_active(False)
            self.logger.debug("Initiating RESET")
            cb = partial(self.resetPlayer)
            self.event_manager.schedule(50, cb)
            return
        # out of lives
        self.logger.debug("Out of Lives!")
        self.onGameOver()

    def doFoodCheck(self, source):
        source_bounds = source.get_bounds()

        for i in range(len(self.food_objects) - 1, -1, -1):
            foodObj = self.food_objects[i]
            food_bounds = foodObj.get_bounds()
            if utilities.intersects(source_bounds, food_bounds):
                # ate food
                self.logger.debug("Ate some food!")
                self.game.get_state().update_score(foodObj.get_score())
                self.food_objects.remove(foodObj)
                self.safe_remove(foodObj)

        if len(self.food_objects) == 0:
            # ate em all
            self.logger.debug("Ate ALL food!")
            self.game.get_state().won = True
            self.logger.debug("You WIN!!!")
            # add some bonus score
            self.game.get_state().finalize_score()
            self.game.get_state().gameover = True
            self.onGameOver()

    def doDeathCheck(self, source):
        dead = False
        bounds = source.get_bounds()
        if bounds.x <= self.layout.border_left:
            self.logger.debug("HIT left wall!")
            dead = True
        elif bounds.x > self.size[0] - bounds.width - self.layout.border_right:
            self.logger.debug("HIT right wall!")
            dead = True
        elif bounds.y <= self.layout.border_top:
            self.logger.debug("HIT top wall!")
            dead = True
        elif bounds.y > self.size[1] - bounds.height - self.layout.border_bottom:
            self.logger.debug("HIT bottom wall!")
            dead = True
        if dead:
            return True
        return False

    def handle_event(self, event, **kwargs):
        # XXX if gameover already, ignore?
        if self.game.get_state().gameover:
            return
        if event.code == eventmanager.GAMEEVENT_POSITION_CHANGED:
            # just assume snake for now, only thing that moves
            if self.doDeathCheck(self.snake):
                self.handleDeath()
                return
            # not dead, check food
            if self.doFoodCheck(self.snake):
                return
