from lib.gameobject import GameObject


class GroupObject(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.ignore_events = False
        self.game_objects = []
        self.layered_game_objects = []
        self.remove_stack = []

    def add_object(self, obj):
        print("Adding ", obj)
        self.game_objects.append(obj)
        obj.set_parent(self)

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
        print("Adding to remove stack: ", obj)
        self.remove_stack.append(obj)

    def dump_game_objects(self):
        print("BEGIN DUMP")
        for obj in self.game_objects:
            print(obj)
        print("END DUMP")

    def finish_safe_remove(self):
        for obj in self.remove_stack:
            # self.dump_game_objects()
            print("Removing from stack: ", obj)
            self.game_objects.remove(obj)
        self.remove_stack.clear()

    def get_object_at(self, x, y):
        print("get_object_at")
        for obj in self.game_objects:
            print("Checking with ", obj)
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
        # clear screen
        if self.background_image:
            self.background_image.draw(surface)
        else:
            surface.fill(self.background_color)
        for obj in self.game_objects:
            obj.draw(surface)
