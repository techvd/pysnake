EVENT_POSITION_CHANGED = 1
EVENT_SCORE_CHANGED = 2
EVENT_LIVES_CHANGED = 3

EVENT_DIRECTION_CHANGE = 11

EVENT_GAME_OVER = 101


class EventManager(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Creating EM")
            cls.__instance = super(EventManager, cls).__new__(cls)
            cls.event_listeners = {}
        return cls.__instance

    def add_event_listener(self, event, listener):
        if event in self.event_listeners:
            # existing entry
            print("EM: adding to existing listener")
            table = self.event_listeners.get(event)
            table.append(listener)
        else:
            print("EM: setting up new listener")
            table = [listener]
            self.event_listeners[event] = table

    def remove_event_listener(self, event, listener):
        table = self.event_listeners.get(event)
        table.remove(listener)

    def clear_event(self, event):
        self.event_listeners.remove(event)

    def raise_event(self, event, args=None):
        table = self.event_listeners[event]
        for listener in table:
            listener.onEvent(event, args)
