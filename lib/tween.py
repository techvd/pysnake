class Tween:
    def __init__(self, game, tween_from, tween_to, tween_duration, auto):
        self.game = game
        self.from_value = tween_from
        self.to_value = tween_to
        self.current_value = self.from_value
        self.duration = tween_duration
        self.elapsed_dt = 0
        self.running = True if auto else False
        self.done = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update(self, dt):
        if self.done or not self.running:
            return
        self.elapsed_dt += dt
        self.current_value += (self.to_value - self.from_value) * (self.duration / self.elapsed_dt)
        print("Tween: ", self.current_value)
        if self.current_value >= self.to_value:
            print("Tween done")
            self.done = True
