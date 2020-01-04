from lib import groupobject
from lib import static
from lib import eventmanager


class GUIButton(static.StaticObject):
    def __init__(self, game):
        super().__init__(game)
        self.on_press_handler = None
        print("GUIButton adding event listener for touch")
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_TOUCH_OBJECT, self)

    def handle_event(self, event, **kwargs):
        print("Button handle_event")
        if event.code == eventmanager.GAMEEVENT_TOUCH_OBJECT:
            self.on_press_handler(self)


class GUIManager(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
