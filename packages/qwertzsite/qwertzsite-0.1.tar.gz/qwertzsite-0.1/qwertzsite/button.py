from dataclasses import dataclass
from typing import Optional
from .text import Text
from .css import CSS
from .elements import Element
from enum import Enum

class ButtonAction(Enum):
    REDIRECT = "redirect"
    NOTIFY = "notify"
    # You can add more action types here in the future
    
class Button(Element):
    text: str
    action: Optional[tuple] = None

    def __init__(self, text):
        if isinstance(text, str):
            self.text = Text(text)
        else:
            self.text = text
        self.css = CSS()

    def setAction(self, action_type: ButtonAction, value: str):
        self.action = (action_type, value)
        return self

    def render(self) -> str:
        button_style = "padding: 10px 20px; cursor: pointer;"
        if self.css:
            button_style += " " + self.css.get_style_string()

        action_attr = ""
        if self.action:
            action_type, value = self.action
            if action_type == ButtonAction.REDIRECT:
                action_attr = f' onclick="window.location.href=\'{value}\'"'
            elif action_type == ButtonAction.NOTIFY:
                action_attr = f' onclick="alert(\'{value}\')"'
        if self.centered:
            container_style = "display: flex; justify-content: center; align-items: center;"
            return f'<div style="{container_style}"><button type="button" style="{button_style}"{action_attr}>{self.text.render()}</button></div>'
        else:
            return f'<button type="button" style="{button_style}"{action_attr}>{self.text.render()}</button>'

    def setCSS(self, css: CSS):
        self.css = css
        return self

    def center(self):
        self.centered = True
        return self