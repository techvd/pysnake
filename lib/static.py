import pygame

from lib import gameobject


class StaticObject(gameobject.GameObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        _sprite = "assets/" + props['image']
        obj = pygame.image.load(_sprite)
        self.pygame_object = pygame.transform.smoothscale(obj, [self.size[0], self.size[1]])
