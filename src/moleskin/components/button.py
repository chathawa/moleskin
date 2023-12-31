from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Union
from pygame import Color

from moleskin.artist import Artist
from moleskin.component import Component
from moleskin.state import State
from moleskin.template import FixedFormTemplate, SelectedState

InitialColor = Color
PressedColor = Color

ButtonForm = Tuple[
    InitialColor,
    PressedColor
]


class ButtonBackgroundTemplate(FixedFormTemplate[ButtonForm]):
    def __init__(self, initial_color: Union[str, Color], pressed_color: Union[str, Color]):
        self._initial_color, self._pressed_color = initial_color, pressed_color
        super().__init__(self._initial_color, self._pressed_color)


class ButtonBackground(Artist[State, SelectedState, ButtonForm]):
    def draw(self, surface, form: ButtonForm, button: Button):
        initial_color, pressed_color = form
        surface.fill(pressed_color if button.is_pressed else initial_color)


class Button(Component, ABC):
    def __init__(
            self,
            template,
            background: ButtonBackgroundTemplate,
            foreground
    ):
        super().__init__(template, background, foreground, ())
        self._is_pressed = False

    @property
    def is_pressed(self):
        return self._is_pressed

    def on_click(self, x, y):
        self._is_pressed = True
