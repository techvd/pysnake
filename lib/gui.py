import logging

import pygame

from lib import groupobject
from lib import staticobject
from lib import eventmanager


class GUIButton(staticobject.StaticObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "BUTTON"
        self.on_press_handler = None
        logging.debug("GUIButton adding event listener for touch")
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_TOUCH_OBJECT, self)

    def handle_event(self, event, **kwargs):
        logging.debug("Button handle_event")
        self.dump()
        if event.code == eventmanager.GAMEEVENT_TOUCH_OBJECT:
            logging.debug(f"Sender: {event.object.get_id()}, Me: {self.get_id()}")
            if event.object.get_id() == self.get_id():
                self.on_press_handler(self)

    def dump(self):
        super().dump()
        logging.debug(f"\tONPRESS: {self.on_press_handler}")


class GUIPanel(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "PANEL"
        self.surface = None
        self.height = 0
        self.elementMap = {}

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        for element in props["elements"]:
            key = element["name"]
            _type = element["type"]
            obj = scene_loader.create_node(_type, element)
            if obj is not None:
                self.elementMap[key] = obj
                self.add_child(obj)
        # print(f"***panel making surface of {self.size}")
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()

    def getAnchor(self):
        return self.anchor

    def getElement(self, name):
        return self.elementMap[name]

    def draw(self, surface):
        super().draw(self.surface)
        surface.blit(self.surface, self.position) # , special_flags=pygame.BLEND_ADD)


class GUIManager(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
