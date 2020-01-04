import sys
import pygame
from functools import partial

from lib import constants
from lib import gamestate
from lib import splash
from lib import gamescene
from lib import gameover
from lib import gameeventhandler
from lib import eventmanager
from lib import sceneloader


class Game:
    def __init__(self):
        self.size = 720, 1280
        pygame.init()
        pygame.display.set_caption('PySnake')
        self.timer_callbacks = {}
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.state = gamestate.GameState()
        self.handler = gameeventhandler.GameEventHandler(self)
        self.loader = sceneloader.SceneLoader(self)
        self.scene = self.loader.load_scene('assets/splash01.json')
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_SPLASH
        eventmanager.EventManager().schedule(2500, partial(self.continueSplash))

    def get_state(self):
        return self.state

    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

    def get_scene(self):
        return self.scene

    def pause(self):
        self.state.paused = True
        self.scene.fade_out()
        print("Paused")

    def isPaused(self):
        return self.state.paused

    def resume(self):
        self.scene.fade_in()
        self.state.paused = False
        print("Resumed")

    def continueSplash(self):
        print("Continue from Splash...")
        self.scene.end_scene()
        self.scene = self.loader.load_scene('assets/level02.json')
        self.scene.dump()
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_GAME
        eventmanager.EventManager().add_event_listener(eventmanager.GAMEEVENT_GAME_OVER, self)

    def handleUserTimer(self, _id):
        pygame.time.set_timer(_id, 0)
        print("RETRIEVE ", _id)
        callback = self.timer_callbacks[_id]
        callback()

    def handleUserEvent(self, _id):
        print("UEV {} received!".format(_id))
        callback = self.timer_callbacks[_id]
        callback()

    def handle_event(self, event, **kwargs):
        print("GAME onEvent ", event)
        if event.code == eventmanager.GAMEEVENT_GAME_OVER:
            self.scene.end_scene()
            self.scene = self.loader.load_scene('assets/gameover.json')
            self.state.scene = self.scene
            self.state.state = gamestate.STATE_GAMEOVER
            # XXX setup callback
            self.scene.ok_btn.on_press_handler = partial(self.on_gameover_ok_pressed)

    def on_gameover_ok_pressed(self, obj):
        print("OK Button is Pressed on gameover scene!")
        self.scene.end_scene()
        sys.exit(0)

    def run(self):
        last_ticks = pygame.time.get_ticks()
        while 1:
            self.clock.tick(60)
            new_ticks = pygame.time.get_ticks()
            dt = new_ticks - last_ticks
            last_ticks = new_ticks
            if dt > 0:
                dt = 1.0 / dt
            # print("Elapsed: ", dt)
            for event in pygame.event.get():
                # XXX temporary
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handler.handle_event(event)
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handler.handle_event(event)
                    continue
                eventmanager.EventManager().handle_event(event)
            if not self.state.paused:
                self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.scene.finish_safe_remove()
