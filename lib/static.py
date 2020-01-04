import pygame

from lib import gameobject


class StaticObject(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        _sprite = "assets/" + props['image']
        obj = pygame.image.load(_sprite)
        self.pygame_object = pygame.transform.smoothscale(obj, [self.size[0], self.size[1]])
        print("Loaded image")
