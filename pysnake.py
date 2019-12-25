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

USER_TIMER = pygame.NOEVENT + 1
EVENT_POSITION_CHANGED = 1


# global functions
def parse_position(_position):
    _coords = _position.split(',')
    x = int(_coords[0])
    y = int(_coords[1])
    return [x, y]


def getRandomColor(colors):
    return colors[random.randint(0, len(colors)-1)]


class GameObject:
    def __init__(self, game, scene, x = 0, y = 0, w = 0, h = 0):
        self.game = game
        self.scene = scene
        self.position = [x, y]
        self.width = w
        self.height = h
        self.update_bounds()

        self.frames = 0
        self.event_listeners = {}

    def get_position(self):
        return self.position

    def get_bounds(self):
        return self.bounds

    def load_props(self, props):
        pass

    def update_bounds(self):
        self.bounds = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

    def move_to(self, x, y):
        self.position[0] = x
        self.position[1] = y
        self.update_bounds()

    def add_event_listener(self, event, listener):
        if event in self.event_listeners:
            # existing entry
            table = self.event_listeners.get(event)
            table.append(listener)
        else:
            table = [listener]
            self.event_listeners[event] = table

    def remove_event_listener(self, event, listener):
        # TODO
        pass

    def raise_event(self, event):
        table = self.event_listeners[event]
        for listener in table:
            listener.onEvent(event, self)

    def update(self, dt):
        pass

    def draw(self, surface):
        if(self.pygame_object):
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
        if(self.done or not self.running):
            return
        self.elapsed_dt += dt
        self.current_value += (self.to_value - self.from_value) * (self.duration / self.elapsed_dt)
        print("Tween: ", self.current_value)
        if(self.current_value >= self.to_value):
            print("Tween done")
            self.done = True


class StaticObject(GameObject):
    def __init__(self, game, scene, sprite, x, y, w, h):
        GameObject.__init__(self, game, scene, x, y, w, h)
        go = pygame.image.load(sprite)
        self.pygame_object = pygame.transform.smoothscale(go, (int(w), int(h)))

    def draw(self, surface):
        #pygame.draw.rect(surface, BLACK, self.bounds)
        GameObject.draw(self, surface)


class Text(GameObject):
    def __init__(self, game, scene, text, color = (255, 255, 255)):
        GameObject.__init__(self, game, scene)
        self.font = pygame.font.Font(None, 36)
        self.color = color
        self.text = text

    def set_text(self, text):
        self.text = text

    def update(self, dt):
        self.pygame_object = self.font.render(self.text, 1, self.color)
        self.rect = self.pygame_object.get_rect()
        screen = self.game.get_screen()
        self.rect.centerx = screen.get_rect().centerx


class PhysicsObject(GameObject):
    def __init__(self, game, scene, x, y, w, h, speed):
        GameObject.__init__(self, game, scene, x, y, w, h)
        self.speed = speed

    def update(self, dt):
        self.position[0] += self.speed[0] * dt
        self.position[1] += self.speed[1] * dt
        #print("New POS ", self.position)


class GameState:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.scene = None
        self.paused = False
        self.won = False
        self.gameover = False


class Scene:
    def __init__(self, game):
        self.game = game
        self.state = game.get_state()
        self.size = game.get_size()
        self.screen = game.get_screen()
        self.ignore_events = False
        self.game_objects = []
        self.remove_stack = []
        self.debug_counter = 0

    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

    def intersects(self, src, dest):
        return src.colliderect(dest)

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
            #self.dump_game_objects()
            print("Removing from stack: ", obj)
            self.game_objects.remove(obj)
        self.remove_stack.clear()


class Food(StaticObject):
    def __init__(self, game, scene, props):
        [x, y] = parse_position(props['position'])
        print("FOOD at {},{}".format(x, y))
        StaticObject.__init__(self, game, scene, "assets/food.png", x, y, CELL_WIDTH, CELL_HEIGHT)
        self.score = int(props['score'])

    def get_score(self):
        return self.score


class Snake(GameObject):
    def __init__(self, game, scene, color, x, y, w, h):
        GameObject.__init__(self, game, scene, x, y, w, h)
        self.color = color
        self.direction = DIRECTION_UP
        self.speed = 50

    def draw(self, surface):
        #print(self.bounds)
        pygame.draw.rect(surface, self.color, self.bounds)

    def set_direction(self, direction):
        self.direction = direction

    def update(self, dt):
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
        self.position = self.scene.clamp_object_position(x, y)
        self.update_bounds()
        self.raise_event(EVENT_POSITION_CHANGED)

CELL_WIDTH = 64
CELL_HEIGHT = 64
BORDER_WIDTH = 32
BORDER_HEIGHT = 32


class GameScene(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)
        self.snake = None
        self.food_objects = []
        #self.build_level()
        self.load_level('assets/level01.json')
        #self.debug = Text(self, "PySnake")
        #self.game_objects.append(self.debug)

    def get_random_position(self):
        x = random.randint(self.bounds.left, self.bounds.right - CELL_WIDTH)
        y = random.randint(self.bounds.top, self.bounds.bottom - CELL_HEIGHT)
        return [x, y]

    def load_level(self, file):
        # XXX get this from file???
        self.bounds = pygame.Rect(BORDER_WIDTH, BORDER_HEIGHT, self.size[0] - BORDER_WIDTH,
                                  self.size[1] - BORDER_HEIGHT)
        with open(file) as level_file:
            _level = json.load(level_file)
            # setup snake next
            _snake = _level['snake']
            [x, y] = parse_position(_snake['position'])
            self.resetPlayer(x, y)
            _food_nodes = _level['food_items']
            for node in _food_nodes:
                food = Food(self.game, self, node)
                self.food_objects.append(food)
                self.game_objects.append(food)

    def spawnPlayer(self, x, y):
        print("Snake at {},{}".format(x, y))
        snake = Snake(self.game, self, YELLOW, x, y, CELL_WIDTH, CELL_HEIGHT)
        return snake

    def resetPlayer(self, x, y):
        if self.snake:
            self.safe_remove(self.snake)
        self.snake = self.spawnPlayer(x, y)
        self.game_objects.append(self.snake)
        self.snake.add_event_listener(EVENT_POSITION_CHANGED, self)
        self.ignore_events = False

    def onGameOver(self):
        print("GAME OVER!!!")
        print("WIN: ", self.state.won)
        print("Score: ", self.state.score)

    def handleDeath(self):
        print("Player is DEAD!")
        self.state.lives = self.state.lives - 1
        if(self.state.lives > 0):
            self.ignore_events = True
            print("Initiating RESET")
            cb = partial(self.resetPlayer, self)
            self.game.schedule(50, USER_TIMER, cb)
            return
        # out of lives
        print("Out of Lives!")
        self.onGameOver()

    def clamp_object_position(self, x, y):
        if x < self.bounds.left:
            x = self.bounds.left
        if x > self.bounds.right - CELL_WIDTH:
            x = self.bounds.right - CELL_WIDTH
        if y < self.bounds.top:
            y = self.bounds.top
        if y > self.bounds.bottom - CELL_HEIGHT:
            y = self.bounds.bottom - CELL_HEIGHT
        return [x, y]

    def doFoodCheck(self, source):
        source_bounds = source.get_bounds()

        for i in range(len(self.food_objects)-1, -1, -1):
            food = self.food_objects[i]
            food_bounds = food.get_bounds()
            if self.intersects(source_bounds, food_bounds):
                # ate food
                print("Ate some food!")
                self.state.score += food.get_score()
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
        source_bounds = source.get_bounds()
        if source_bounds.x <= BORDER_WIDTH:
            print("HIT left wall!")
            dead = True
        elif source_bounds.x > self.size[0] - CELL_WIDTH - BORDER_WIDTH:
            print("HIT right wall!")
            dead = True
        elif source_bounds.y <= BORDER_HEIGHT:
            print("HIT top wall!")
            dead = True
        elif source_bounds.y > self.size[1] - CELL_HEIGHT - BORDER_HEIGHT:
            print("HIT bottom wall!")
            dead = True
        if(dead):
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

    def update(self, dt):
        if self.state.paused:
            return
        if self.ignore_events:
            #print("Ignoring events...")
            return
        for obj in self.game_objects:
            obj.update(dt)

    def draw(self):
        # clear screen
        self.screen.fill(GREY)

        # draw the border. since the width and height could be different,
        # we have to draw them independently
        pygame.draw.line(self.screen, ORANGE, [0, 0], [0, self.size[1]], BORDER_WIDTH*2)
        pygame.draw.line(self.screen, ORANGE, [0, 0], [self.size[0], 0], BORDER_HEIGHT*2)
        pygame.draw.line(self.screen, ORANGE, [self.size[0], 0], [self.size[0], self.size[1]], BORDER_WIDTH * 2)
        pygame.draw.line(self.screen, ORANGE, [0, self.size[1]], [self.size[0], self.size[1]], BORDER_HEIGHT * 2)

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

    def schedule(self, millis, id, callback):
        self.timer_callbacks[id] = callback
        pygame.time.set_timer(id, millis)

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
            #print("Elapsed: ", dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    self.handleUserEvent(event.id)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.resume() if self.state.paused else self.pause()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                self.handler.onEvent(event)
            self.scene.update(dt)
            self.scene.draw()
            pygame.display.flip()
            self.scene.finish_safe_remove()


game = Game()
game.run()
