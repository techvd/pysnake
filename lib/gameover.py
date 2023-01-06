import logging
from lib import basescene


class GameOverScene(basescene.BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.name = "GAMEOVER"
        self.panel = None
        logging.debug("GAMEOVER created!!")

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        for key in props:
            if 'panel' == key:
                self.panel = scene_loader.create_node('panel', props[key])
                self.add_child(self.panel)
                score = self.panel.getElement("text_score")
                _score = self.game.get_state().score
                score.set_text("Score: {}".format(_score), True)
                bonus = self.panel.getElement("text_bonus")
                _bonus = self.game.get_state().bonus
                bonus.set_text("Bonus: {}".format(_bonus), True)
                total = self.panel.getElement("text_total")
                _total = self.game.get_state().score + self.game.get_state().bonus
                total.set_text("Total: {}".format(_total), True)

    def get_gui_element(self, name):
        return self.panel.getElement(name)
