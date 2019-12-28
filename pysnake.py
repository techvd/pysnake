import sys
import json
import pygame
import random
from functools import partial

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
ORANGE = 255, 165, 0
YELLOW = 255, 255, 0
GREY = 128, 128, 128
STEEL = 224, 223, 219

DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4

USER_TIMER_ONCE = pygame.USEREVENT + 1
EVENT_POSITION_CHANGED = 1
EVENT_SCORE_CHANGED = 2
EVENT_LIVES_CHANGED = 3

# global functions
def parse_value(prop):
    return int(prop)


def parse_2dvec(prop):
    xy = prop.split(',')
    x = int(xy[0])
    y = int(xy[1])
    return [x, y]


def parse_3dvec(prop):
    xyz = prop.split(',')
    x = int(xyz[0])
    y = int(xyz[1])
    z = int(xyz[2])
    return [x, y, z]


def parse_color(prop):
    _color = parse_3dvec(prop)
    return pygame.Color(_color[0], _color[1], _color[2])


def intersects(src, dest):
    return src.colliderect(dest)


def get_random_color(colors):
    return colors[random.randint(0, len(colors) - 1)]


class EventManager(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Creating EM")
            cls.__instance = super(EventManager, cls).__new__(cls)
            cls.event_listeners = {}
        return cls.__instance

    def add_event_listener(self, event, listener):
        if event in self.event_listeners:
            # existing entry
            print("EM: adding to existing listener")
            table = self.event_listeners.get(event)
            table.append(listener)
        else:
            print("EM: setting up new listener")
            table = [listener]
            self.event_listeners[event] = table

    def remove_event_listener(self, event, listener):
        table = self.event_listeners.get(event)
        table.remove(listener)

    def clear_event(self, event):
        self.event_listeners.remove(event)

    def raise_event(self, event, caller=None):
        table = self.event_listeners[event]
        for listener in table:
            listener.onEvent(event, caller)


class GameObject:
    def __init__(self, game, scene, props=None):
        self.parent = None
        self.pygame_object = None
        self.game = game
        self.scene = scene
        self.position = [0, 0]
        self.size = [0, 0]
        self.bounds = None
        self.active = True
        self.visible = True
        self.load_props(props)

        self.frames = 0

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_position(self):
        return self.position

    def get_bounds(self):
        return self.bounds

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def is_visible(self):
        return self.visible

    def set_visible(self, vis):
        self.visible = vis

    def load_props(self, props):
        if props is not None:
            if 'position' in props:
                self.position = parse_2dvec(props['position'])
            if 'size' in props:
                self.size = parse_2dvec(props['size'])
            self.update_bounds()

    def update_bounds(self):
        self.bounds = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def move_to(self, x, y):
        self.position[0] = x
        self.position[1] = y
        self.update_bounds()

    def update(self, dt):
        pass

    def draw(self, surface):
        if self.pygame_object:
            surface.blit(self.pygame_object, self.bounds)


class Tween:
    def __init__(self, game, tween_from, tween_to, tween_duration, auto):
        self.game = game
        self.from_value = tween_from
        self.to_value = tween_to
        self.current_value = self.from_value
        self.duration = tween_duration
        self.elapsed_dt = 0
        self.running = True if auto else False
        self.done = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update(self, dt):
        if self.done or not self.running:
            return
        self.elapsed_dt += dt
        self.current_value += (self.to_value - self.from_value) * (self.duration / self.elapsed_dt)
        print("Tween: ", self.current_value)
        if self.current_value >= self.to_value:
            print("Tween done")
            self.done = True


class StaticObject(GameObject):
    def __init__(self, game, scene, props, sprite):
        super().__init__(game, scene, props)
        obj = pygame.image.load(sprite)
        self.pygame_object = pygame.transform.smoothscale(obj, [self.size[0], self.size[1]])

    def draw(self, surface):
        #pygame.draw.rect(surface, BLACK, self.bounds)
        GameObject.draw(self, surface)


class Text(GameObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        _weight = parse_value(props['weight'])
        self.anchor = props['anchor']
        self.font = pygame.font.Font(None, _weight)
        self.color = parse_color(props['color'])
        self.text = ""

    def set_text(self, text, adjust = False):
        self.text = text
        self.pygame_object = self.font.render(self.text, 1, self.color)
        self.bounds = self.pygame_object.get_rect()
        if adjust:
            self.adjust_layout()

    def adjust_layout(self):
        _pb = self.parent.get_bounds()
        print("PB: ", _pb)
        if self.anchor == "left":
            _x = _pb.left + 5 # just for spacing
            _y = _pb.top + (_pb.height - self.bounds.height) / 2
        if self.anchor == "right":
            _x = _pb.right - self.bounds.width - 5 # just for spacing
            _y = _pb.top + (_pb.height - self.bounds.height) / 2
        self.move_to(_x, _y)


class PhysicsObject(GameObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        self.speed = parse_value(props['speed'])

    def update(self, dt):
        self.position[0] += self.speed[0] * dt
        self.position[1] += self.speed[1] * dt
        # print("New POS ", self.position)


class GroupObject(GameObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        self.ignore_events = False
        self.game_objects = []
        self.remove_stack = []

    def add_object(self, obj):
        print("Adding ", obj)
        self.game_objects.append(obj)
        obj.set_parent(self)

    def safe_remove(self, obj):
        # just append to stack
        print("Adding to remove stack: ", obj)
        self.remove_stack.append(obj)

    def dump_game_objects(self):
        print("BEGIN DUMP")
        for obj in self.game_objects:
            print(obj)
        print("END DUMP")

    def finish_safe_remove(self):
        for obj in self.remove_stack:
            # self.dump_game_objects()
            print("Removing from stack: ", obj)
            self.game_objects.remove(obj)
        self.remove_stack.clear()

    def update(self, dt):
        if self.ignore_events:
            return
        for obj in self.game_objects:
            #print("Updating ", obj)
            obj.update(dt)

    def draw(self, surface):
        # draw objects
        for obj in self.game_objects:
            obj.draw(surface)


class Scene(GroupObject):
    def __init__(self, game, props):
        super().__init__(game, self, props)
        self.state = game.get_state()
        self.size = game.get_size()
        self.bounds = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.screen = game.get_screen()
        self.debug_counter = 0

    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen


class Food(StaticObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props, "assets/food.png")
        self.score = parse_value(props['score'])

    def get_score(self):
        return self.score


class Snake(GameObject):
    def __init__(self, game, scene, color, props):
        super().__init__(game, scene, props)
        self.starting_position = self.position
        self.color = color
        self.direction = DIRECTION_UP
        self.speed = parse_value(props['speed'])

    def draw(self, surface):
        # print(self.bounds)
        pygame.draw.rect(surface, self.color, self.bounds)

    def set_direction(self, direction):
        self.direction = direction

    def reset(self):
        self.move_to(self.starting_position[0], self.starting_position[1])

    def update(self, dt):
        if not self.active:
            return
        dx = dy = 0
        if self.direction == DIRECTION_RIGHT:
            dx = self.speed * dt
        if self.direction == DIRECTION_LEFT:
            dx = -self.speed * dt
        if self.direction == DIRECTION_DOWN:
            dy = self.speed * dt
        if self.direction == DIRECTION_UP:
            dy = -self.speed * dt
        x = self.position[0]
        x += dx
        y = self.position[1]
        y += dy
        self.position = self.scene.clamp_object_position(self, x, y)
        self.update_bounds()
        EventManager().raise_event(EVENT_POSITION_CHANGED, self)


class Layout:
    def __init__(self, props):
        _layout = props['layout']
        _border = _layout['border']
        self.border_left = _border['left']
        self.border_top = _border['top']
        self.border_right = _border['right']
        self.border_bottom = _border['bottom']
        self.border_color = parse_color(_border['color'])


class Hud(GroupObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        self.location = props['location']
        self.height = props['height']
        scene_size = self.scene.get_size()
        # TODO revisit this part
        if self.location == "top":
            self.bounds = pygame.Rect(0, 0, scene_size[0], self.height)
        self.color = parse_color(props['color'])
        _score = props['score']
        self.score = Text(self.game, self.scene, _score)
        self.add_object(self.score)
        self.score.set_text("Score: 0", True)
        _lives = props['lives']
        self.lives = Text(self.game, self.scene, _lives)
        self.add_object(self.lives)
        self.lives.set_text("Lives: 3", True)
        # finally, listen to changes
        EventManager().add_event_listener(EVENT_SCORE_CHANGED, self)
        EventManager().add_event_listener(EVENT_LIVES_CHANGED, self)

    def onEvent(self, event, caller):
        print("HUD onEvent: ", event)
        if event == EVENT_SCORE_CHANGED:
            _state = self.game.get_state()
            self.score.set_text("Score: {}".format(_state.score), True)
        if event == EVENT_LIVES_CHANGED:
            _state = self.game.get_state()
            self.lives.set_text("Lives: {}".format(_state.lives), True)

    def draw(self, surface):
        # first draw the background
        # XXX make some assumptions?
        if self.location == "top":
            size = self.scene.get_size()
            pygame.draw.line(surface, self.color, [0, self.height/2], [size[0], self.height/2], self.height)
        super().draw(surface)


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game, None)
        self.name = "UNKNOWN"
        self.background_color = GREY
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
            self.background_color = parse_color(_level['background'])
            # process layout
            self.layout = Layout(_level)
            self.bounds = pygame.Rect(self.layout.border_left, self.layout.border_top,
                                      self.size[0] - self.layout.border_right,
                                      self.size[1] - self.layout.border_bottom)
            # process hud
            _hud = _level['hud']
            self.hud = Hud(self.game, self, _hud)
            self.add_object(self.hud)
            # setup snake next
            _snake = _level['snake']
            snake = Snake(self.game, self, YELLOW, _snake)
            self.setupPlayer(snake)
            _food_nodes = _level['food_items']
            print("Foods: #{}".format(len(_food_nodes)))
            for node in _food_nodes:
                food = Food(self.game, self, node)
                self.food_objects.append(food)
                self.add_object(food)

    def setupPlayer(self, snake):
        self.snake = snake
        self.add_object(self.snake)
        EventManager().add_event_listener(EVENT_POSITION_CHANGED, self)
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

    def handleDeath(self):
        print("Player is DEAD!")
        self.state.update_lives(-1)
        if self.state.lives > 0:
            self.ignore_events = True
            self.snake.set_active(False)
            print("Initiating RESET")
            cb = partial(self.resetPlayer)
            self.game.schedule(50, USER_TIMER_ONCE, cb)
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
            food = self.food_objects[i]
            food_bounds = food.get_bounds()
            if intersects(source_bounds, food_bounds):
                # ate food
                print("Ate some food!")
                self.state.update_score(food.get_score())
                self.food_objects.remove(food)
                self.safe_remove(food)

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
        if (dead):
            return True
        return False

    def onEvent(self, event, source):
        # if gameover already, ignore
        if self.state.gameover:
            return
        # just assume snake for now, only thing that moves
        if self.doDeathCheck(source):
            self.handleDeath()
            return
        # not dead, check food
        if self.doFoodCheck(source):
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

        # draw objects
        for obj in self.game_objects:
            obj.draw(self.screen)


class GameEventHandler:
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.scene.snake.set_direction(DIRECTION_DOWN)
            if event.key == pygame.K_UP:
                self.scene.snake.set_direction(DIRECTION_UP)
            if event.key == pygame.K_LEFT:
                self.scene.snake.set_direction(DIRECTION_LEFT)
            if event.key == pygame.K_RIGHT:
                self.scene.snake.set_direction(DIRECTION_RIGHT)


class GameState:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.scene = None
        self.paused = False
        self.won = False
        self.gameover = False

    def update_score(self, delta):
        self.score += delta
        EventManager().raise_event(EVENT_SCORE_CHANGED)

    def update_lives(self, delta):
        self.lives += delta
        EventManager().raise_event(EVENT_LIVES_CHANGED)


class Game:
    def __init__(self):
        self.size = 720, 1280
        pygame.init()
        pygame.display.set_caption('PySnake')
        self.timer_callbacks = {}
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.state = GameState()
        self.scene = GameScene(self)
        self.state.scene = self.scene
        self.handler = GameEventHandler(self, self.scene)

    def get_state(self):
        return self.state

    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

    def pause(self):
        self.state.paused = True
        print("Paused")

    def isPaused(self):
        return self.state.paused

    def resume(self):
        self.state.paused = False

    def schedule(self, millis, _id, callback):
        print("SCHEDULE ", _id)
        self.timer_callbacks[_id] = callback
        pygame.time.set_timer(_id, millis)

    def handleUserTimer(self, _id):
        pygame.time.set_timer(_id, 0)
        print("RETRIEVE ", _id)
        callback = self.timer_callbacks[_id]
        callback()

    def handleUserEvent(self, id):
        print("UEV {} received!".format(id))
        callback = self.timer_callbacks[id]
        callback()

    def run(self):
        last_ticks = pygame.time.get_ticks()
        while 1:
            self.clock.tick(60)
            new_ticks = pygame.time.get_ticks()
            dt = new_ticks - last_ticks
            last_ticks = new_ticks
            if dt > 0:
                dt = 1.0 / dt
            # print("Elapsed: ", dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == USER_TIMER_ONCE:
                    print("USER_TIMER_ONCE!!!")
                    self.handleUserTimer(USER_TIMER_ONCE)
                if event.type == pygame.USEREVENT:
                    self.handleUserEvent(event.id)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.resume() if self.state.paused else self.pause()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print("POS: ", pos)
                self.handler.onEvent(event)
            self.scene.update(dt)
            self.scene.draw()
            pygame.display.flip()
            self.scene.finish_safe_remove()


_game = Game()
_game.run()
