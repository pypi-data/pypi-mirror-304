from dataclasses import dataclass, field
from typing import Optional
from .css import CSS

@dataclass
class Element:
    content: str
    css: Optional[CSS] = None
    centered: bool = False

    def setCSS(self, css: CSS):
        self.css = css
        return self

    def center(self):
        self.centered = True
        return self

    def render(self) -> str:
        style = self.css.get_style_string() if self.css else ""
        if self.centered:
            centering_style = "display: flex; justify-content: center; align-items: center;"
            style = f"{centering_style} {style}"
        return f'<div style="{style}">{self.content}</div>'
    