import pygame
from lib import constants
from lib import eventmanager


class GameEventHandler:
    def __init__(self, game):
        self.game = game

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                eventmanager.EventManager().raise_event(eventmanager.EVENT_DIRECTION_CHANGE,
                                                        {"direction": constants.DIRECTION_DOWN})
            if event.key == pygame.K_UP:
                eventmanager.EventManager().raise_event(eventmanager.EVENT_DIRECTION_CHANGE,
                                                        {"direction": constants.DIRECTION_UP})
            if event.key == pygame.K_LEFT:
                eventmanager.EventManager().raise_event(eventmanager.EVENT_DIRECTION_CHANGE,
                                                        {"direction": constants.DIRECTION_LEFT})
            if event.key == pygame.K_RIGHT:
                eventmanager.EventManager().raise_event(eventmanager.EVENT_DIRECTION_CHANGE,
                                                        {"direction": constants.DIRECTION_RIGHT})
