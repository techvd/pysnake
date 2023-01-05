import logging

import pygame
from lib.groupobject import GroupObject
from lib import eventmanager


class Hud(GroupObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "HUD"
        self.has_background = False
        self.location = ''
        self.height = 0
        self.score = None
        self.lives = None
        # finally, listen to changes
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_SCORE_CHANGED, self)
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_LIVES_CHANGED, self)

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.score = self.panel.getElement("text_score")
        self.score.set_text("Score: 0", True)
        self.lives = self.panel.getElement("text_lives")
        self.lives.set_text("Lives: 3", True)
        # finally, listen to changes
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_SCORE_CHANGED, self)
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_LIVES_CHANGED, self)

    def handle_event(self, event, **kwargs):
        logging.debug("HUD handle_event: ", event)
        if event.code == eventmanager.GAMEEVENT_SCORE_CHANGED:
            _state = self.game.get_state()
            self.score.set_text("Score: {}".format(_state.score), True)
        if event.code == eventmanager.GAMEEVENT_LIVES_CHANGED:
            _state = self.game.get_state()
            self.lives.set_text("Lives: {}".format(_state.lives), True)
