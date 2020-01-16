from lib import gameobject
from lib import constants
from lib import utilities


class GroupObject(gameobject.GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.ignore_events = False
        self.background_color = constants.BLACK
        self.background = None
        self.game_objects = []
        self.layered_game_objects = []
        self.sorted_layers = None
        self.remove_stack = []

    def dump(self):
        self.logger.debug(self)
        for obj in self.game_objects:
            obj.dump()

    def load_props(self, scene_loader, props):
        super().load_props(scene_loader, props)
        if props is not None:
            if 'background_color' in props:
                self.background_color = utilities.parse_color(props['background_color'])
            if 'background' in props:
                self.background = scene_loader.create_node('background', props['background'])
                self.add_child(self.background)

    def add_child(self, obj):
        self.game_objects.append(obj)
        obj.set_parent(self)
        # resort objects by layer
        self.game_objects.sort(key=lambda x: x.layer)

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
        self.logger.debug("Adding to remove stack: ", obj)
        self.remove_stack.append(obj)

    def dump_game_objects(self):
        self.logger.debug("BEGIN DUMP")
        for obj in self.game_objects:
            obj.dump()
        self.logger.debug("END DUMP")

    def finish_safe_remove(self):
        for obj in self.remove_stack:
            # self.dump_game_objects()
            self.logger.debug("Removing from stack: ", obj)
            self.game_objects.remove(obj)
        self.remove_stack.clear()

    def get_object_at(self, x, y):
        for i in range(len(self.game_objects)-1, -1, -1):
            obj = self.game_objects[i]
            self.logger.debug("Checking with ", obj)
            if obj.is_within(x, y):
                return obj
        if self.is_within(x, y):
            return self
        return None

    def update(self, dt):
        if self.ignore_events:
            return
        for obj in self.game_objects:
            obj.update(dt)

    def draw(self, surface):
        if not self.visible:
            return
        if self.background:
            self.background.draw(surface)
        else:
            surface.fill(self.background_color, self.bounds)
        #for obj in self.game_objects:
        for i in range(0, len(self.game_objects)):
            self.game_objects[i].draw(surface)
