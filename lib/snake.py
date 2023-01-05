import logging
import pygame

from lib import gameobject
from lib import constants
from lib import utilities
from lib import eventmanager


class Snake(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "SNAKE"
        self.starting_position = [0, 0]
        self.direction = constants.DIRECTION_UP
        self.color = constants.GREEN
        self.speed = 50
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_DIRECTION_CHANGE, self)

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'speed' in props:
                self.speed = utilities.parse_value(props['speed'])
            if 'color' in props:
                self.color = utilities.parse_color(props['color'])
        self.starting_position = self.position

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def set_direction(self, direction):
        self.direction = direction

    def reset(self):
        self.move_to(self.starting_position[0], self.starting_position[1])

    def handle_event(self, event, **kwargs):
        logging.debug(f"** SNAKE handle_event: {event}...")
        if event.code == eventmanager.GAMEEVENT_DIRECTION_CHANGE:
            self.set_direction(event.direction)

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
        self.position = self.parent.clamp_object_position(self, x, y)
        self.update_bounds()
        self.event_manager.raise_event(eventmanager.GAMEEVENT_POSITION_CHANGED)
