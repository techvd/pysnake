import logging
import pygame

from lib import gameobject
from lib import constants
from lib import utilities


class GroupObject(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "GROUP"
        self.ignore_events = False
        self.has_background = False
        self.background_color = constants.BLACK
        self.background = None
        self.elementMap = {}
        self.game_objects = []
        self.layered_game_objects = []
        self.sorted_layers = None
        self.remove_stack = []

    def dump(self):
        super().dump()
        for obj in self.game_objects:
            obj.dump()

    def is_container(self):
        return True

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if 'background_color' in props:
            self.has_background = True
            self.background_color = utilities.parse_color(props['background_color'])
        if 'background' in props:
            self.has_background = True
            self.background = scene_loader.create_node('background', props['background'])
            self.add_child(self.background)
        if 'elements' in props:
            for element in props["elements"]:
                key = element["name"]
                _type = element["type"]
                # self.inject_props(element)
                obj = scene_loader.create_node(_type, element)
                if obj is not None:
                    self.elementMap[key] = obj
                    self.add_child(obj)

    def inject_props(self, node):
        # main thing is adjusting position
        # print(f"ADJ {self.name} mypos is {self.position}")
        if 'position' in node:
            pos = utilities.parse_2dvec(node['position'])
            new_pos = [self.position[0] + pos[0], self.position[1] + pos[1]]
            node['position'] = new_pos
            # print(f"ADJ {node['name']} {pos} to {new_pos}")

    def add_child(self, obj):
        self.game_objects.append(obj)
        obj.set_parent(self)
        # resort objects by layer
        self.game_objects.sort(key=lambda x: x.layer)

    def getElement(self, name):
        return self.elementMap[name]

    def clamp_object_position(self, obj, x, y):
        obj_bounds = obj.get_bounds()
        if x < self.bounds.left:
            x = self.bounds.left
        if x > self.bounds.right - obj_bounds.width:
            x = self.bounds.right - obj_bounds.width
        if y < self.bounds.top:
            y = self.bounds.top
        if y > self.bounds.bottom - obj_bounds.height:
            y = self.bounds.bottom - obj_bounds.height
        return [x, y]

    def safe_remove(self, obj):
        # just append to stack
        logging.debug(f"Adding to remove stack: {obj}")
        self.remove_stack.append(obj)

    def finish_safe_remove(self):
        for obj in self.remove_stack:
            # self.dump_game_objects()
            logging.debug(f"Removing from stack: {obj}")
            self.game_objects.remove(obj)
        self.remove_stack.clear()

    def get_object_at(self, x, y):
        for i in range(len(self.game_objects)-1, -1, -1):
            obj = self.game_objects[i]
            logging.debug(f"Checking with {obj}...")
            sub_obj = obj.get_object_at(x, y)
            if sub_obj is not None:
                return sub_obj
        if self.is_within(x, y):
            return self
        return None

    def update(self, dt):
        if self.ignore_events:
            return
        super().update(dt)
        for obj in self.game_objects:
            obj.update(dt)

    def draw(self, surface, state):
        if not self.visible:
            return
        if self.has_background:
            if self.background:
                self.background.draw(surface, state)
            else:
                if state['debugFrame']:
                    print(f"GO BGFILL {self.bounds}")
                bg_bounds = pygame.Rect(0, 0, self.size[0], self.size[1])
                # surface.fill(self.background_color, bg_bounds)
                pygame.draw.rect(surface, self.background_color, bg_bounds, 0, 32)
        # for obj in self.game_objects:
        for i in range(0, len(self.game_objects)):
            if state['debugFrame']:
                print(f"GO CALL DRAW ON {self.game_objects[i].name}")
            self.game_objects[i].draw(surface, state)

    def do_fade(self, _from, _to):
        _incr = 8
        if _from > _to:
            _incr = -8
        _w = self.size[0]
        _h = self.size[1]
        _fade = pygame.Surface((_w, _h))
        _fade.fill((0, 0, 0))
        for alpha in range(_from, _to, _incr):
            _fade.set_alpha(alpha)
            self.draw()
            self.screen.blit(_fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)

    def fade_out(self):
        self.do_fade(0, 160)

    def fade_in(self):
        self.do_fade(160, 0)
