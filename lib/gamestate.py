from lib import eventmanager


STATE_SPLASH = 1
STATE_MENU = 2
STATE_GAME = 3
STATE_GAMEOVER = 4
STATE_OPTIONS = 11


class GameState:
    def __init__(self, game):
        self.game = game
        self.logger = game.get_logger()
        self.event_manager = game.get_event_manager()
        self.lives = 1
        self.score = 0
        self.bonus = 0
        self.state = None
        self.scene = None
        self.paused = False
        self.won = False
        self.gameover = False

    def update_score(self, delta):
        self.score += delta
        self.event_manager.raise_event(eventmanager.GAMEEVENT_SCORE_CHANGED)

    def finalize_score(self):
        if self.lives == 3:
            # all lives left
            self.bonus = 5000
        elif self.lives == 2:
            self.bonus = 3000
        elif self.lives == 1:
            self.bonus = 1000
        self.event_manager.raise_event(eventmanager.GAMEEVENT_SCORE_CHANGED)

    def update_lives(self, delta):
        self.lives += delta
        self.event_manager.raise_event(eventmanager.GAMEEVENT_LIVES_CHANGED)
