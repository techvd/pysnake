import sys
import logging
import argparse
from functools import partial
import pygame

from lib import gamestate
from lib import gameeventhandler
from lib import eventmanager
from lib import sceneloader
from lib import debugscene


FORMAT_STRING = '%(asctime)s %(message)s'
LEVEL_FILE = 'assets/levels/level05.json'


class Game:
    def __init__(self, argv):
        self.arguments = self.process_args()
        if self.arguments.debug:
            print("Turning on debug logging")
            logging.basicConfig(format=FORMAT_STRING, level=logging.DEBUG)
        else:
            logging.basicConfig(format=FORMAT_STRING, level=logging.WARNING)

        self.size = 720, 1280
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
        self.scene.dump()
        # self.scene = debugscene.DebugScene(self)
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_SPLASH
        self.event_manager.schedule(1000, partial(self.continueSplash))

    def process_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="store_true", help="Display version")
        parser.add_argument("--debug", action="store_true", help="Turn on debug mode")
        return parser.parse_args()

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
        logging.info("Paused")

    def isPaused(self):
        return self.state.paused

    def resume(self):
        self.scene.fade_in()
        self.state.paused = False
        logging.info("Resumed")

    def continueSplash(self):
        logging.info("Continue from Splash...")
        self.scene.end_scene()
        self.scene = self.loader.load_scene(LEVEL_FILE)
        self.state.scene = self.scene
        self.state.state = gamestate.STATE_GAME
        self.event_manager.add_event_listener(eventmanager.GAMEEVENT_GAME_OVER, self)

    def handleUserTimer(self, _id):
        pygame.time.set_timer(_id, 0)
        logging.info("RETRIEVE ", _id)
        callback = self.timer_callbacks[_id]
        callback()

    def handleUserEvent(self, _id):
        logging.info("UEV {} received!".format(_id))
        callback = self.timer_callbacks[_id]
        callback()

    def handle_event(self, event, **kwargs):
        logging.debug(f"GAME onEvent {event}")
        if event.code == eventmanager.GAMEEVENT_GAME_OVER:
            self.scene.end_scene()
            self.scene = self.loader.load_scene('assets/screens/gameover.json')
            self.state.scene = self.scene
            self.state.state = gamestate.STATE_GAMEOVER
            # XXX setup callback
            self.scene.get_gui_element("btn_quit").on_press_handler = partial(self.on_gameover_quit_pressed)
            self.scene.get_gui_element("btn_retry").on_press_handler = partial(self.on_gameover_retry_pressed)

    def on_gameover_quit_pressed(self, obj):
        logging.info("Quit Button is Pressed on gameover scene!")
        self.scene.end_scene()
        sys.exit(0)

    def on_gameover_retry_pressed(self, obj):
        logging.info("Retry Button is Pressed on gameover scene!")
        self.continueSplash() # XXX for now

    def run(self):
        while 1:
            dt = self.clock.tick(60)
            fps = self.clock.get_fps()
            if dt > 0:
                dt = 1.0 / dt
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
            # print("\n\nFRAME BEGIN")
            self.scene.draw(self.screen)
            # print("FRAME END")
            pygame.display.flip()
            self.scene.finish_safe_remove()
