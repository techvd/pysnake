import sys
import pygame
from functools import partial

from lib import logger
from lib import gamestate
from lib import gameeventhandler
from lib import eventmanager
from lib import sceneloader
from lib import debugscene


class Game:
    def __init__(self, argv):
        self.argv = argv
        self.size = 720, 1280
        self.logger = logger.Logger(self)
        self.event_manager = eventmanager.EventManager(self)
        pygame.init()
        pygame.display.set_caption('PySnake')
        self.timer_callbacks = {}
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
        self.state = gamestate.GameState(self)
        self.handler = gameeventhandler.GameEventHandler(self)
        self.loader = sceneloader.SceneLoader(self)
        self.scene = self.loader.load_scene('assets/screens/splash01.json')
        # self.scene = debugscene.DebugScene(self)
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_SPLASH
        self.event_manager.schedule(1000, partial(self.continueSplash))
        self.process_args()

    def process_args(self):
        pass

    def get_logger(self):
        return self.logger

    def get_event_manager(self):
        return self.event_manager

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
        self.logger.info("Paused")

    def isPaused(self):
        return self.state.paused

    def resume(self):
        self.scene.fade_in()
        self.state.paused = False
        self.logger.info("Resumed")

    def continueSplash(self):
        self.logger.info("Continue from Splash...")
        self.scene.end_scene()
        self.scene = self.loader.load_scene('assets/levels/level03.json')
        self.scene.dump()
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_GAME
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_GAME_OVER, self)

    def handleUserTimer(self, _id):
        pygame.time.set_timer(_id, 0)
        self.logger.info("RETRIEVE ", _id)
        callback = self.timer_callbacks[_id]
        callback()

    def handleUserEvent(self, _id):
        self.logger.info("UEV {} received!".format(_id))
        callback = self.timer_callbacks[_id]
        callback()

    def handle_event(self, event, **kwargs):
        self.logger.info("GAME onEvent ", event)
        if event.code == eventmanager.GAMEEVENT_GAME_OVER:
            self.scene.end_scene()
            self.scene = self.loader.load_scene('assets/screens/gameover.json')
            self.state.scene = self.scene
            self.state.state = gamestate.STATE_GAMEOVER
            # XXX setup callback
            self.scene.ok_btn.on_press_handler = partial(self.on_gameover_ok_pressed)

    def on_gameover_ok_pressed(self, obj):
        self.logger.info("OK Button is Pressed on gameover scene!")
        self.scene.end_scene()
        sys.exit(0)

    def run(self):
        while 1:
            dt = self.clock.tick(60)
            fps = self.clock.get_fps()
            #print("FPS: ", fps)
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
                self.event_manager.handle_event(event)
            if not self.state.paused:
                self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.scene.finish_safe_remove()
