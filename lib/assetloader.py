import pygame


class AssetLoader:
    _root = "assets"
    _landscape = False

    @staticmethod
    def load_image(image):
        path = AssetLoader._root + "/images/"
        path = path + image
        if AssetLoader._landscape:
            path = path + "_l"
        path = path + ".png"
        return pygame.image.load(path)
