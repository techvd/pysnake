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
    if isinstance(prop, list):
        return prop
    parts = prop.split(',')
    x = int(parts[0])
    y = int(parts[1])
    z = int(parts[2])
    a = 255
    if len(parts) > 3:
        a = int(parts[3])
    return pygame.Color(x, y, z, a)


def intersects(src, dest):
    return src.colliderect(dest)


def get_random_color(colors):
    return colors[random.randint(0, len(colors) - 1)]
