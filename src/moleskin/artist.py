from abc import ABC, abstractmethod
from typing import Tuple, Generic
from pygame import Surface
from moleskin.layout import Position
from moleskin.state import State, SelectedState
from moleskin.template import Template, Form


class Artist(ABC, Generic[State, SelectedState, Form]):
    _origin: Position = (0, 0)

    def __init__(self, template: Template[State, SelectedState, Form]):
        self._template = template

    @property
    def template(self):
        return self._template

    def bind_template(self, state: State, component):
        return self._template.bind(self._template.select_state(state), component) if self._template else None

    @abstractmethod
    def draw(self, surface: Surface, form: Form, component):
        pass

    def __getstate__(self):
        return self._template


Artists = Tuple[Artist, ...]


__all__ = ['Form', 'Artist', 'Artists']
