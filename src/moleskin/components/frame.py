from abc import ABC, abstractmethod
from typing import Callable, Generic
from pygame import Surface
from moleskin.component import Component
from moleskin.state import State, SelectedState
from moleskin.template import Form


class Frame(ABC, Generic[State, SelectedState, Form]):
    def __init__(self, root: Component[State, SelectedState, Form]):
        self._root = root

    @property
    def root(self):
        return self._root

    def loop(self, screen: Surface):
        while self.draw(screen):
            self._root.draw(screen, self.state)

    @abstractmethod
    def draw(self, screen: Surface) -> bool:
        pass

    @abstractmethod
    @property
    def state(self) -> State:
        pass


__all__ = ['Frame']
