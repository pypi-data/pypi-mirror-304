class CSS:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def add(self, property: str, value: str):
        self.properties[property] = value
        return self

    def get_style_string(self):
        return "; ".join([f"{k}: {v}" for k, v in self.properties.items()])

class Flags:
    FONT_SIZE = "font-size"
    COLOR = "color"
    BACKGROUND_COLOR = "background-color"
    MARGIN = "margin"
    PADDING = "padding"
    # Add more CSS properties as needed