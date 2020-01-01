from lib import utilities


class Layout:
    def __init__(self, props):
        _layout = props['layout']
        _border = _layout['border']
        self.border_left = _border['left']
        self.border_top = _border['top']
        self.border_right = _border['right']
        self.border_bottom = _border['bottom']
        self.border_color = utilities.parse_color(_border['color'])
