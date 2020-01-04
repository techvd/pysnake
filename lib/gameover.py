from functools import partial

from lib import scene


class GameOverScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game)
        self.ok_btn = None
        self.score = None
        print("GAMEOVER created!!")

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'button' in props:
                self.ok_btn = scene_loader.create_node('button', props['button'])
                self.add_object(self.ok_btn)
            if 'score' in props:
                self.score = scene_loader.create_node('score', props['score'])
                self.add_object(self.score)
                _score = self.game.get_state().score
                self.score.set_text("Score: {}".format(_score), True)
