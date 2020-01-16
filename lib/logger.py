import datetime
import inspect


LOG_NONE = 0
LOG_ERROR = 1
LOG_INFO = 2
LOG_VERBOSE = 4
LOG_DEBUG = 8


class Logger:
    def __init__(self, game):
        self.game = game
        self.level = LOG_INFO

    def log(self, *args):
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'), end=' ')
        print(*args)

    def debug(self, *args):
        if self.level & LOG_DEBUG:
            self.log(*args)

    def error(self, *args):
        if self.level & LOG_ERROR:
            self.log(*args)

    def info(self, *args):
        if self.level & LOG_INFO:
            self.log(*args)
