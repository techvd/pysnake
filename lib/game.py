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
        #self.scene = gamescene.GameScene(self)
        self.scene = splash.SplashScene(self)
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_SPLASH
        self.schedule(2500, constants.USER_TIMER_SPLASH, partial(self.continueSplash))

    def get_state(self):
        return self.state

    def get_size(self):
        return self.size

    def get_screen(self):
        return self.screen

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

    def schedule(self, millis, _id, callback):
        print("SCHEDULE ", _id)
        self.timer_callbacks[_id] = callback
        pygame.time.set_timer(_id, millis)

    def continueSplash(self):
        print("Continue from Splash...")
        print(self)

        self.scene = gamescene.GameScene(self)
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_GAME
        eventmanager.EventManager().add_event_listener(eventmanager.EVENT_GAME_OVER, self)

    def handleUserTimer(self, _id):
        pygame.time.set_timer(_id, 0)
        print("RETRIEVE ", _id)
        callback = self.timer_callbacks[_id]
        callback()

    def handleUserEvent(self, _id):
        print("UEV {} received!".format(_id))
        callback = self.timer_callbacks[_id]
        callback()

    def onEvent(self, event, caller):
        print("GAME onEvent ", event)
        if event == eventmanager.EVENT_GAME_OVER:
            self.scene = gameover.GameOverScene(self)
            self.state.scene = self.scene
            self.state.state = gamestate.STATE_GAME
            self.handler = None

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
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == constants.USER_TIMER_ONCE or event.type == constants.USER_TIMER_SPLASH:
                    print("USER_TIMER!!!")
                    self.handleUserTimer(event.type)
                if event.type == pygame.USEREVENT:
                    self.handleUserEvent(event.id)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.scene.fade_out()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.resume() if self.state.paused else self.pause()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print("POS: ", pos)
                if self.handler is not None:
                    self.handler.onEvent(event)
            if not self.state.paused:
                self.scene.update(dt)
                self.scene.draw()
                pygame.display.flip()
            self.scene.finish_safe_remove()
