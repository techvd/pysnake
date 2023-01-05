import pygame
from lib import constants
from lib import eventmanager


class GameEventHandler:
    def __init__(self, game):
        self.game = game
        self.event_manager = game.get_event_manager()

    def handle_event(self, event, **kwargs):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.event_manager.raise_event(eventmanager.GAMEEVENT_DIRECTION_CHANGE,
                                                        direction=constants.DIRECTION_DOWN)
            if event.key == pygame.K_UP:
                self.event_manager.raise_event(eventmanager.GAMEEVENT_DIRECTION_CHANGE,
                                                        direction=constants.DIRECTION_UP)
            if event.key == pygame.K_LEFT:
                self.event_manager.raise_event(eventmanager.GAMEEVENT_DIRECTION_CHANGE,
                                                        direction=constants.DIRECTION_LEFT)
            if event.key == pygame.K_RIGHT:
                self.event_manager.raise_event(eventmanager.GAMEEVENT_DIRECTION_CHANGE,
                                                        direction=constants.DIRECTION_RIGHT)
        if event.type == pygame.MOUSEBUTTONDOWN:
            _scene = self.game.get_scene()
            _obj = _scene.get_object_at(event.pos[0], event.pos[1])
            if _obj is not None:
                self.event_manager.raise_event(eventmanager.GAMEEVENT_TOUCH_OBJECT,
                                                        object=_obj)
