from lib import constants
from lib import eventmanager


STATE_SPLASH = 1
STATE_MENU = 2
STATE_GAME = 3
STATE_GAMEOVER = 4
STATE_OPTIONS = 11


class GameState:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.state = None
        self.scene = None
        self.paused = False
        self.won = False
        self.gameover = False

    def update_score(self, delta):
        self.score += delta
        eventmanager.EventManager().raise_event(eventmanager.GAMEEVENT_SCORE_CHANGED)

    def update_lives(self, delta):
        self.lives += delta
        eventmanager.EventManager().raise_event(eventmanager.GAMEEVENT_LIVES_CHANGED)
