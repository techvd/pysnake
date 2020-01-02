import pygame
import json
from functools import partial

from lib import scene
from lib import layout
from lib import utilities
from lib import snake
from lib import food
from lib import constants
from lib import hud
from lib import eventmanager


class GameScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game, None)
        self.name = "UNKNOWN"
        self.background_color = constants.GREY
        self.snake = None
        self.layout = None
        self.hud = None
        self.bounds = None
        self.food_objects = []
        self.load_level('assets/level02.json')
        # self.debug = Text(self, "PySnake")
        # self.game_objects.append(self.debug)

    def get_layout(self):
        return self.layout

    def load_level(self, file):
        with open(file) as level_file:
            _level = json.load(level_file)
            self.name = _level['name']
            self.background_color = utilities.parse_color(_level['background_color'])
            # process layout
            self.layout = layout.Layout(_level)
            self.bounds = pygame.Rect(self.layout.border_left, self.layout.border_top,
                                      self.size[0] - self.layout.border_right,
                                      self.size[1] - self.layout.border_bottom)
            # process hud
            _hud = _level['hud']
            self.hud = hud.Hud(self.game, self, _hud)
            self.add_object(self.hud)
            # setup snake next
            _snake = _level['snake']
            _snakeObj = snake.Snake(self.game, self, constants.YELLOW, _snake)
            self.setupPlayer(_snakeObj)
            _food_nodes = _level['food_items']
            print("Foods: #{}".format(len(_food_nodes)))
            for node in _food_nodes:
                foodObj = food.Food(self.game, self, node)
                self.food_objects.append(foodObj)
                self.add_object(foodObj)

    def setupPlayer(self, snake):
        self.snake = snake
        self.add_object(self.snake)
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_POSITION_CHANGED, self)
        self.ignore_events = False

    def resetPlayer(self):
        print("???")
        print(self)
        self.snake.reset()
        self.ignore_events = False
        self.snake.set_active(True)
        # what else to do here?

    def onGameOver(self):
        self.ignore_events = True
        self.snake.set_active(False)
        print("GAME OVER!!!")
        print("WIN: ", self.state.won)
        print("Score: ", self.state.score)
        eventmanager.EventManager().raise_event(eventmanager.GAMEEVENT_GAME_OVER)

    def handleDeath(self):
        print("Player is DEAD!")
        self.state.update_lives(-1)
        if self.state.lives > 0:
            self.ignore_events = True
            self.snake.set_active(False)
            print("Initiating RESET")
            cb = partial(self.resetPlayer)
            eventmanager.EventManager().schedule(50, cb)
            return
        # out of lives
        print("Out of Lives!")
        self.onGameOver()

    def clamp_object_position(self, obj, x, y):
        objbounds = obj.get_bounds()
        if x < self.bounds.left:
            x = self.bounds.left
        if x > self.bounds.right - objbounds.width:
            x = self.bounds.right - objbounds.width
        if y < self.bounds.top:
            y = self.bounds.top
        if y > self.bounds.bottom - objbounds.height:
            y = self.bounds.bottom - objbounds.height
        return [x, y]

    def doFoodCheck(self, source):
        source_bounds = source.get_bounds()

        for i in range(len(self.food_objects) - 1, -1, -1):
            foodObj = self.food_objects[i]
            food_bounds = foodObj.get_bounds()
            if utilities.intersects(source_bounds, food_bounds):
                # ate food
                print("Ate some food!")
                self.state.update_score(foodObj.get_score())
                self.food_objects.remove(foodObj)
                self.safe_remove(foodObj)

        if len(self.food_objects) == 0:
            # ate em all
            print("Ate ALL food!")
            self.state.won = True
            print("You WIN!!!")
            self.state.gameover = True
            self.onGameOver()

    def doDeathCheck(self, source):
        dead = False
        bounds = source.get_bounds()
        if bounds.x <= self.layout.border_left:
            print("HIT left wall!")
            dead = True
        elif bounds.x > self.size[0] - bounds.width - self.layout.border_right:
            print("HIT right wall!")
            dead = True
        elif bounds.y <= self.layout.border_top:
            print("HIT top wall!")
            dead = True
        elif bounds.y > self.size[1] - bounds.height - self.layout.border_bottom:
            print("HIT bottom wall!")
            dead = True
        if dead:
            return True
        return False

    def handle_event(self, event, **kwargs):
        # XXX if gameover already, ignore?
        if self.state.gameover:
            return
        #print(event)
        if event.code == eventmanager.GAMEEVENT_POSITION_CHANGED:
            # just assume snake for now, only thing that moves
            if self.doDeathCheck(self.snake):
                self.handleDeath()
                return
            # not dead, check food
            if self.doFoodCheck(self.snake):
                return

    def draw(self):
        # clear screen
        self.screen.fill(self.background_color)

        # draw the border. since the width and height could be different,
        # we have to draw them independently
        pygame.draw.line(self.screen, self.layout.border_color, [0, self.layout.border_top/2-1],
                         [self.size[0], self.layout.border_top/2-1], self.layout.border_top)
        pygame.draw.line(self.screen, self.layout.border_color, [0, self.size[1]-self.layout.border_bottom/2],
                         [self.size[0], self.size[1]-self.layout.border_bottom/2], self.layout.border_bottom)
        pygame.draw.line(self.screen, self.layout.border_color, [self.layout.border_left/2-1, 0],
                         [self.layout.border_left/2-1, self.size[1]], self.layout.border_left)
        pygame.draw.line(self.screen, self.layout.border_color, [self.size[0]-self.layout.border_right/2, 0],
                         [self.size[0]-self.layout.border_right/2, self.size[1]], self.layout.border_right)

        super().draw(self.screen)
