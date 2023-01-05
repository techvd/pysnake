import logging
import pygame


GAMEEVENT = pygame.USEREVENT + 1
TIMEREVENT = pygame.USEREVENT + 2

GAMEEVENT_POSITION_CHANGED = 1
GAMEEVENT_SCORE_CHANGED = 2
GAMEEVENT_LIVES_CHANGED = 3

GAMEEVENT_DIRECTION_CHANGE = 11

GAMEEVENT_TOUCH_OBJECT = 21

GAMEEVENT_GAME_OVER = 101


class EventManager:
    def __init__(self, game):
        self.game = game
        self.event_listeners = {}
        self.timer_callback = None

    def add_event_listener(self, event, listener):
        if event in self.event_listeners:
            # existing entry
            logging.debug("EM: adding to existing listener")
            table = self.event_listeners.get(event)
            table.append(listener)
        else:
            logging.debug("EM: setting up new listener")
            table = [listener]
            self.event_listeners[event] = table

    def remove_event_listener(self, event, listener):
        table = self.event_listeners.get(event)
        table.remove(listener)

    def clear_event(self, event):
        self.event_listeners.remove(event)

    def raise_event(self, event, **kwargs):
        # logging.debug(f"Raising event {event}")
        pygame.event.post(pygame.event.Event(GAMEEVENT, code=event, **kwargs))

    def handle_event(self, event, **kwargs):
        if event.type == TIMEREVENT and self.timer_callback is not None:
            pygame.time.set_timer(TIMEREVENT, 0)
            cb = self.timer_callback
            self.timer_callback = None
            cb()
            return
        if event.type == GAMEEVENT:
            code = event.code
            if event.code not in self.event_listeners:
                return
            table = self.event_listeners[event.code]
            for listener in table:
                listener.handle_event(event)

    def schedule(self, millis, callback):
        self.timer_callback = callback
        pygame.time.set_timer(TIMEREVENT, millis)
