from functools import partial

from lib import tilescene


class GameOverScene(tilescene.TileScene):
    def __init__(self, game):
        super().__init__(game)
        self.ok_btn = None
        self.score = None
        self.bonus = None
        self.total = None
        self.logger.debug("GAMEOVER created!!")

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'button' in props:
                self.ok_btn = scene_loader.create_node('button', props['button'])
                self.add_child(self.ok_btn)
            if 'text_score' in props:
                self.score = scene_loader.create_node('text_score', props['text_score'])
                self.add_child(self.score)
                _score = self.game.get_state().score
                self.score.set_text("Score: {}".format(_score), True)
            if 'text_bonus' in props:
                self.bonus = scene_loader.create_node('text_bonus', props['text_bonus'])
                self.add_child(self.bonus)
                _bonus = self.game.get_state().bonus
                self.bonus.set_text("Bonus: {}".format(_bonus), True)
            if 'text_total' in props:
                self.total = scene_loader.create_node('text_total', props['text_total'])
                self.add_child(self.total)
                _total = self.game.get_state().score + self.game.get_state().bonus
                self.total.set_text("Total: {}".format(_total), True)
