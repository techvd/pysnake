import logging
from lib import basescene


class GameOverScene(basescene.BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.name = "GAMEOVER"
        self.panels = {}
        logging.debug("GAMEOVER created!!")

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        self.set_values()

    def set_values(self):
        score = self.get_gui_element("score", "text_score")
        _score = self.game.get_state().score
        score.set_text("Score: {}".format(_score), True)
        bonus = self.get_gui_element("score", "text_bonus")
        _bonus = self.game.get_state().bonus
        bonus.set_text("Bonus: {}".format(_bonus), True)
        total = self.get_gui_element("score", "text_total")
        _total = self.game.get_state().score + self.game.get_state().bonus
        total.set_text("Total: {}".format(_total), True)

    def get_gui_element(self, name1, name2):
        panel = self.getElement(name1)
        return panel.getElement(name2)
