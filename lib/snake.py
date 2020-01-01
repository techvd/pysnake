import pygame

from lib import gameobject
from lib import constants
from lib import utilities
from lib import eventmanager


class Snake(gameobject.GameObject):
    def __init__(self, game, scene, color, props):
        super().__init__(game, scene, props)
        self.starting_position = self.position
        self.color = color
        self.direction = constants.DIRECTION_UP
        self.speed = utilities.parse_value(props['speed'])
        eventmanager.EventManager().add_event_listener(eventmanager.EVENT_DIRECTION_CHANGE, self)

    def draw(self, surface):
        # print(self.bounds)
        pygame.draw.rect(surface, self.color, self.bounds)

    def set_direction(self, direction):
        self.direction = direction

    def reset(self):
        self.move_to(self.starting_position[0], self.starting_position[1])

    def onEvent(self, event, args):
        print("** SNAKE onEvent: ", event)
        if event == eventmanager.EVENT_DIRECTION_CHANGE:
            self.set_direction(args['direction'])

    def update(self, dt):
        if not self.active:
            return
        dx = dy = 0
        if self.direction == constants.DIRECTION_RIGHT:
            dx = self.speed * dt
        if self.direction == constants.DIRECTION_LEFT:
            dx = -self.speed * dt
        if self.direction == constants.DIRECTION_DOWN:
            dy = self.speed * dt
        if self.direction == constants.DIRECTION_UP:
            dy = -self.speed * dt
        x = self.position[0]
        x += dx
        y = self.position[1]
        y += dy
        self.position = self.scene.clamp_object_position(self, x, y)
        self.update_bounds()
        eventmanager.EventManager().raise_event(eventmanager.EVENT_POSITION_CHANGED, self)
