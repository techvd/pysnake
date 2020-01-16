from lib import groupobject
from lib import static
from lib import eventmanager


class GUIButton(static.StaticObject):
    def __init__(self, game):
        super().__init__(game)
        self.on_press_handler = None
        self.logger.debug("GUIButton adding event listener for touch")
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_TOUCH_OBJECT, self)

    def handle_event(self, event, **kwargs):
        self.logger.debug("Button handle_event")
        self.logger.debug(self)
        if event.code == eventmanager.GAMEEVENT_TOUCH_OBJECT:
            self.logger.debug("Sender: ", event.object.get_id())
            self.logger.debug("Me: ", self.get_id())
            if event.object.get_id() == self.get_id():
                self.on_press_handler(self)


class GUIManager(groupobject.GroupObject):
    def __init__(self, game):
        super().__init__(game)
