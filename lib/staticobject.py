import pygame

from lib import gameobject
from lib import assetloader


class StaticObject(gameobject.GameObject):
    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        obj = assetloader.AssetLoader.load_image(props['image'])
        self.pygame_object = pygame.transform.smoothscale(obj, [self.size[0], self.size[1]]).convert_alpha()
