from typing import Tuple, Union
from pygame import Color
from moleskin.artist import Artist
from moleskin.state import State, SelectedState
from moleskin.template import FixedFormTemplate, Template

BackgroundColorForm = Tuple[
    Color
]


class BackgroundColorTemplate(FixedFormTemplate[BackgroundColorForm]):
    @classmethod
    def _hexcode_to_color(cls, hexcode: str):
        try:
            if '#' in hexcode:
                return cls._hexcode_to_color(hexcode.replace('#', ''))

            byte_count = len(hexcode) / 2

            if byte_count not in (3, 4):
                raise ValueError("hexcode length is neither 6 (RGB) nor 8 (RGBA)")

            return Color(*(
                int(hexcode[2 * n: 2 * (n + 1)], 0x10)
                for n in range(int(byte_count))
            ))
        except (UserWarning, ValueError) as ex:
            raise UserWarning(f"invalid hexcode '{hexcode}'") from ex

    def __init__(self, color: Union[str, Color]):
        self._color = self._hexcode_to_color(color) if type(color) is str else color
        super().__init__(self._color)

    @property
    def color(self):
        return self._color


class BackgroundColor(Artist[State, SelectedState, BackgroundColorForm]):
    def __init__(self, template: Union[BackgroundColorForm, BackgroundColorTemplate]):
        super().__init__(template if isinstance(template, Template) else BackgroundColorTemplate(*template))

    def draw(self, surface, form: BackgroundColorForm, component):
        color, = form
        surface.fill(color)


__all__ = ['BackgroundColorForm', 'BackgroundColorTemplate', 'BackgroundColor']
