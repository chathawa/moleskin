from abc import ABC, abstractmethod
from typing import Tuple

from pygame import Surface

Size = Tuple[
    int,
    int
]

Sizes = Tuple[Size, ...]

Position = Tuple[
    int,
    int
]

Positions = Tuple[Position, ...]

Arrangement = Tuple[
    Size,
    Positions
]


class Layout(ABC):
    @abstractmethod
    def arrange(self, surface: Surface, child_sizes: Sizes) -> Arrangement:
        pass


__all__ = ['Size', 'Sizes', 'Position', 'Positions', 'Layout']
