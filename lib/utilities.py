import random
import pygame


# global functions
def parse_value(prop):
    return int(prop)


def parse_2dvec(prop):
    if isinstance(prop, list):
        return prop
    xy = prop.split(',')
    x = int(xy[0])
    y = int(xy[1])
    return [x, y]


def parse_3dvec(prop):
    if isinstance(prop, list):
        return prop
    xyz = prop.split(',')
    x = int(xyz[0])
    y = int(xyz[1])
    z = int(xyz[2])
    return [x, y, z]


def parse_color(prop):
    _color = parse_3dvec(prop)
    return pygame.Color(_color[0], _color[1], _color[2])


def intersects(src, dest):
    return src.colliderect(dest)


def get_random_color(colors):
    return colors[random.randint(0, len(colors) - 1)]
