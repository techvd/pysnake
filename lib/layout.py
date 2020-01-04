from lib import utilities


class Layout:
    def __init__(self):
        self.border_left = 0
        self.border_right = 0
        self.border_top = 0
        self.border_bottom = 0
        self.border_color = None

    def load_props(self, scene_loader, props):
        _border = props['border']
        self.border_left = _border['left']
        self.border_top = _border['top']
        self.border_right = _border['right']
        self.border_bottom = _border['bottom']
        self.border_color = utilities.parse_color(_border['color'])
