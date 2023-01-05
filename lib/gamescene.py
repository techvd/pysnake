import logging
from functools import partial

from lib import tilescene
from lib import utilities
from lib import eventmanager


class GameScene(tilescene.TileScene):
    def __init__(self, game):
        super().__init__(game)
        self.hud = None
        self.snake = None
        self.food_objects = []
        self.obstacles = []
        # self.debug = Text(self, "PySnake")
        # self.game_objects.append(self.debug)
        self.pause()

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        snake_node = props['snake']
        snake_obj = self.create_object(scene_loader, snake_node, 'snake')
        self.setupPlayer(snake_obj)
        if 'food_items' in props:
            _food_nodes = props['food_items']
            logging.debug("Foods: #{}".format(len(_food_nodes)))
            for food_node in _food_nodes:
                food_obj = self.create_object(scene_loader, food_node, 'food')
                if food_obj is None:
                    logging.error(f"Failed to create food node")
                    continue
                self.add_food(food_obj)
        if 'walls' in props:
            _wall_nodes = props['walls']
            logging.debug("Walls: #{}".format(len(_wall_nodes)))
            for wall_node in _wall_nodes:
                wall_obj = self.create_object(scene_loader, wall_node, 'wall')
                if wall_obj is None:
                    logging.error(f"Failed to create wall node")
                    continue
                self.add_obstacle(wall_obj)
        self.setup_hud(scene_loader, props['hud'])

    def setup_hud(self, scene_loader, props):
        # also need to anchor hud
        # XXX should this be more generic at the add_child level of group?
        _anchor = props['anchor']
        _height = props['height']
        if _anchor == "top":
            props['position'] = "0, 0"
            props["size"] = f"{self.size[0]}, {_height}"
        self.hud = scene_loader.create_node('panel', props)
        self.add_child(self.hud)
        score = self.hud.getElement("text_score")
        score.set_text("Score: 0", True)
        lives = self.hud.getElement("text_lives")
        lives.set_text("Lives: 3", True)
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_SCORE_CHANGED, self)
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_LIVES_CHANGED, self)

    def add_snake(self, snake):
        self.snake = snake
        self.setupPlayer(snake)

    def add_food(self, food):
        self.food_objects.append(food)
        self.add_child(food)

    def add_obstacle(self, obj):
        self.obstacles.append(obj)
        self.add_child(obj)

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
        logging.debug("GAME OVER!!!")
        self.event_manager.raise_event(eventmanager.GAMEEVENT_GAME_OVER)

    def handleDeath(self):
        logging.debug("Player is DEAD!")
        self.game.get_state().update_lives(-1)
        if self.game.get_state().lives > 0:
            self.ignore_events = True
            self.snake.set_active(False)
            logging.debug("Initiating RESET")
            cb = partial(self.resetPlayer)
            self.event_manager.schedule(50, cb)
            return
        # out of lives
        logging.debug("Out of Lives!")
        self.onGameOver()

    def doFoodCheck(self, source):
        source_bounds = source.get_bounds()

        for i in range(len(self.food_objects) - 1, -1, -1):
            foodObj = self.food_objects[i]
            food_bounds = foodObj.get_bounds()
            if utilities.intersects(source_bounds, food_bounds):
                # ate food
                logging.debug("Ate some food!")
                self.game.get_state().update_score(foodObj.get_score())
                self.food_objects.remove(foodObj)
                self.safe_remove(foodObj)

        if len(self.food_objects) == 0:
            # ate em all
            logging.debug("Ate ALL food!")
            self.game.get_state().won = True
            logging.debug("You WIN!!!")
            # add some bonus score
            self.game.get_state().finalize_score()
            self.game.get_state().gameover = True
            self.onGameOver()

    def doDeathCheck(self, source):
        bounds = source.get_bounds()
        # check bounds first
        if bounds.x <= self.layout.border_left:
            logging.warning("HIT left wall!")
            return True
        elif bounds.x > self.size[0] - bounds.width - self.layout.border_right:
            logging.warning("HIT right wall!")
            return True
        elif bounds.y <= self.layout.border_top:
            logging.warning("HIT top wall!")
            return True
        elif bounds.y > self.size[1] - bounds.height - self.layout.border_bottom:
            logging.warning("HIT bottom wall!")
            return True
        # didn't run into walls, check obstacles next
        for i in range(len(self.obstacles)):
            obs = self.obstacles[i]
            obs_bounds = obs.get_bounds()
            if utilities.intersects(bounds, obs_bounds):
                # we hit an obstacle
                logging.warning("Hit an obstacle")
                return True
        return False

    def handle_event(self, event, **kwargs):
        # XXX if gameover already, ignore?
        if self.game.get_state().gameover:
            return
        if event.code == eventmanager.GAMEEVENT_SCORE_CHANGED:
            _state = self.game.get_state()
            score = self.hud.getElement("text_score")
            score.set_text("Score: {}".format(_state.score), True)
        elif event.code == eventmanager.GAMEEVENT_LIVES_CHANGED:
            _state = self.game.get_state()
            lives = self.hud.getElement("text_lives")
            lives.set_text("Lives: {}".format(_state.lives), True)
        elif event.code == eventmanager.GAMEEVENT_POSITION_CHANGED:
            # just assume snake for now, only thing that moves
            if self.doDeathCheck(self.snake):
                self.handleDeath()
                return
            # not dead, check food
            if self.doFoodCheck(self.snake):
                return
