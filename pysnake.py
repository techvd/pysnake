import sys
import math
import pygame
import random
from functools import partial

EVENT_POSITON_CHANGED = 1

class GameObject:
    def __init__(self, game, x = 0, y = 0, w = 0, h = 0):
        self.game = game
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
            surface.blit(self.pygame_object, self.position)

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
    def __init__(self, game, sprite, x, y, w, h):
        GameObject.__init__(self, game, x, y, w, h)
        go = pygame.image.load(sprite)
        self.pygame_object = pygame.transform.smoothscale(go, (int(w), int(h)))

    def draw(self, surface):
        surface.blit(self.pygame_object, self.position)

class Text(GameObject):
    def __init__(self, game, text, color = (255, 255, 255)):
        GameObject.__init__(self, game)
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
    def __init__(self, game, x, y, w, h, speed):
        GameObject.__init__(self, game, x, y, w, h)
        self.speed = speed

    def update(self, dt):
        self.position[0] += self.speed[0] * dt
        self.position[1] += self.speed[1] * dt
        #print("New POS ", self.position)

class Cell(GameObject):
    def __init__(self, game, color, x, y, width, height):
        GameObject.__init__(self, game, x, y, width, height)
        self.color = color

    def move_to(self, x, y):
        print("*E: unexpected cell:moveto")

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

class Food(StaticObject):
    def __init__(self, game, ix, iy):
        self.index_x = ix
        self.index_y = iy
        cw = game.cell_width
        ch = game.cell_height
        x = ix * game.cell_width
        y = iy * game.cell_height
        StaticObject.__init__(self, game, "assets/food.png", x, y, game.cell_width, game.cell_height)

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
ORANGE = 255, 165, 0
YELLOW = 255, 255, 0
GREY = 128, 128, 128
STEEL = 224, 223, 219

def getRandomColor(colors):
    return colors[random.randint(0, len(colors)-1)]

DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4

USER_TIMER = pygame.NOEVENT + 1


class Snake(GameObject):
    def __init__(self, game, color, ix, iy):
        self.index_x = ix
        self.index_y = iy
        cw = game.cell_width
        ch = game.cell_height
        x = ix * game.cell_width
        y = iy * game.cell_height
        GameObject.__init__(self, game, x, y, game.cell_width, game.cell_height)
        self.color = color
        self.direction = DIRECTION_RIGHT
        self.speed = 50

    def draw(self, surface):
        #print(self.bounds)
        pygame.draw.rect(surface, self.color, self.bounds)

    def update(self, dt):
        dx = dy = 0
        if self.direction == DIRECTION_RIGHT:
            dx = self.speed * dt
        self.position[0] += dx
        self.position[1] += dy
        self.update_bounds()
        self.raise_event(EVENT_POSITON_CHANGED)


class GameState:
    def __init__(self):
        self.lives = 50
        self.scene = None
        self.paused = False
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


CELL_WIDTH = 64
CELL_HEIGHT = 64
BORDER_WIDTH = 32
BORDER_HEIGHT = 32


class GameScene(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)
        self.snake = None
        self.cells = []
        self.food = []
        self.build_level()
        #self.debug = Text(self, "PySnake")
        #self.game_objects.append(self.debug)

    def build_level(self):
        # setup cells first
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.rows = int(math.floor((self.size[1] - BORDER_HEIGHT * 2) / self.cell_height))
        self.columns = int(math.floor((self.size[0] - BORDER_WIDTH * 2) / self.cell_width))
        self.border_height = int((self.size[1] - self.rows * self.cell_height) / 2)
        self.border_width = int((self.size[0] - self.columns * self.cell_width) / 2)

        print("Cell DIMS {}x{}".format(self.cell_width, self.cell_height))
        print("Border DIMS {}x{}".format(self.border_width, self.border_height))
        print("Level DIMS {}x{}".format(self.rows, self.columns))
        next_y = self.border_height
        for y in range(self.rows):
            next_x = self.border_width
            for x in range(self.columns):
                print("CELL {},{} at {},{}".format(y, x, next_x, next_y))
                cell = Cell(self, STEEL, next_x, next_y, self.cell_width, self.cell_height)
                self.game_objects.append(cell)
                next_x += self.cell_width
            next_y += self.cell_height
        # setup food items
        for i in range(10):
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.columns-1)
            print("FOOD {} at {},{}".format(i, x, y))
            food = Food(self, x, y)
            self.food.append(food)
            self.game_objects.append(food)
        # setup snake next
        self.resetPlayer()

    def spawnPlayer(self):
        snake_x = random.randint(0, self.rows - 1)
        snake_y = random.randint(0, self.columns - 1)
        print("Snake at {},{}".format(snake_x, snake_y))
        snake = Snake(self, YELLOW, snake_x, snake_y)
        return snake

    def resetPlayer(self):
        if self.snake:
            self.safe_remove(self.snake)
        # basically respawn player somewhere randomly
        self.snake = self.spawnPlayer()
        self.game_objects.append(self.snake)
        self.snake.add_event_listener(EVENT_POSITON_CHANGED, self)
        self.ignore_events = False

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
        print("Game really ended")
        self.state.gameover = True

    def doFoodCheck(self, source):
        source_bounds = source.get_bounds()

        for i in range(len(self.food)-1, 0, -1):
            food = self.food[i]
            food_bounds = food.get_bounds()
            if self.intersects(source_bounds, food_bounds):
                # ate food
                print("Ate some food!")
                self.food.remove(food)
                self.safe_remove(food)
                break

    def doDeathCheck(self, source):
        dead = False
        source_bounds = source.get_bounds()
        if source_bounds.x <= 0:
            print("HIT left wall!")
            dead = True
        elif source_bounds.x > self.size[0] - self.cell_width:
            print("HIT right wall!")
            dead = True
        elif source_bounds.y <= 0:
            print("HIT top wall!")
            dead = True
        elif source_bounds.y > self.size[1] - self.cell_height:
            print("HIT bottom wall!")
            dead = True
        if(dead):
            self.handleDeath()
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
        self.screen.fill(BLACK)
        # draw the border. since the width and height could be different,
        # we have to draw them independently
        pygame.draw.line(self.screen, ORANGE, [0, 0], [0, self.size[1]], self.border_width*2)
        pygame.draw.line(self.screen, ORANGE, [0, 0], [self.size[0], 0], self.border_height*2)
        pygame.draw.line(self.screen, ORANGE, [self.size[0], 0], [self.size[0], self.size[1]], self.border_width * 2)
        pygame.draw.line(self.screen, ORANGE, [0, self.size[1]], [self.size[0], self.size[1]], self.border_height * 2)

        # draw objects
        for obj in self.game_objects:
            obj.draw(self.screen)

        # XXX draw lines now
        next_x = self.border_width + self.cell_width
        for i in range(self.columns):
            pygame.draw.line(self.screen, GREY, [next_x, self.border_height], [next_x, self.size[1] - self.border_height])
            next_x += self.cell_width
        next_y = self.border_height + self.cell_height
        for i in range(self.rows):
            pygame.draw.line(self.screen, GREY, [self.border_width, next_y], [self.size[0] - self.border_width, next_y])
            next_y += self.cell_height


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
            self.scene.update(dt)
            self.scene.draw()
            pygame.display.flip()
            self.scene.finish_safe_remove()


game = Game()
game.run()
