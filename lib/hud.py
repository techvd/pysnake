import pygame
from lib.groupobject import GroupObject
from lib import utilities
from lib.textobject import Text
from lib import eventmanager
from lib import constants
from lib import sceneloader


class Hud(GroupObject):
    def __init__(self, game):
        super().__init__(game)
        self.location = ''
        self.height = 0
        self.score = None
        self.lives = None
        # finally, listen to changes
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_SCORE_CHANGED, self)
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_LIVES_CHANGED, self)

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.location = props['location']
        self.height = props['height']
        scene_size = scene_loader.get_scene().get_size()
        # TODO revisit this part
        if self.location == "top":
            self.bounds = pygame.Rect(0, 0, scene_size[0], self.height)
        self.score = scene_loader.create_node('score', props['score'])
        self.add_object(self.score)
        self.score.set_text("Score: 0", True)
        self.lives = scene_loader.create_node('lives', props['lives'])
        self.add_object(self.lives)
        self.lives.set_text("Lives: 3", True)
        # finally, listen to changes
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_SCORE_CHANGED, self)
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_LIVES_CHANGED, self)

    def handle_event(self, event, **kwargs):
        print("HUD handle_event: ", event)
        if event.code == eventmanager.GAMEEVENT_SCORE_CHANGED:
            _state = self.game.get_state()
            self.score.set_text("Score: {}".format(_state.score), True)
        if event.code == eventmanager.GAMEEVENT_LIVES_CHANGED:
            _state = self.game.get_state()
            self.lives.set_text("Lives: {}".format(_state.lives), True)

    def draw(self, surface):
        # first draw the background
        # XXX make some assumptions?
        if self.location == "top":
            size = self.scene.get_size()
            pygame.draw.line(surface, self.color, [0, self.height/2], [size[0], self.height/2], self.height)
        super().draw(surface)
