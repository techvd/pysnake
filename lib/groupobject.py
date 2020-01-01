from lib.gameobject import GameObject


class GroupObject(GameObject):
    def __init__(self, game, scene, props):
        super().__init__(game, scene, props)
        self.ignore_events = False
        self.game_objects = []
        self.remove_stack = []

    def add_object(self, obj):
        print("Adding ", obj)
        self.game_objects.append(obj)
        obj.set_parent(self)

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

    def update(self, dt):
        if self.ignore_events:
            return
        for obj in self.game_objects:
            #print("Updating ", obj)
            obj.update(dt)

    def draw(self, surface):
        # draw objects
        for obj in self.game_objects:
            obj.draw(surface)
