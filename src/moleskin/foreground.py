from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Tuple, Union, Dict, cast

import pygame.font
from pygame import Color, Surface
from pygame.font import Font
from gui.bases.artist import Artist
from gui.bases.state import StateModel
from gui.bases.template import Template, FixedFormTemplate

State = TypeVar('State', bound=StateModel)
SelectedState = TypeVar('SelectedState')

Text = str
Antialias = bool


class Alignment(ABC):
    @abstractmethod
    def offset(self, surface: Surface, text: str, font: Font) -> int:
        pass


class LeftAlignment(Alignment):
    def offset(self, surface, text, font):
        return 0


class CenterAlignment(Alignment):
    def offset(self, surface, text, font):
        width, _ = font.size(text)
        return -width // 2


class RightAlignment(Alignment):
    def offset(self, surface, text, font):
        width, _ = font.size(text)
        return -width


ForegroundForm = Tuple[
    Font,
    Text,
    Antialias,
    Color,
    Color,
    Alignment
]


class ForegroundTemplate(FixedFormTemplate[ForegroundForm]):
    _font_cache: Dict[str, Font] = {}

    @classmethod
    def _resolve_font(cls, name: str, size: int):
        try:
            font = cls._font_cache[name]
        except KeyError:
            font = cls._font_cache[name] = pygame.font.SysFont(name, size)

        return font

    def __init__(
            self,
            font: Union[Tuple[str, float], Font],
            text: str,
            antialias: bool,
            color: Color,
            bg_color: Color,
            alignment: Alignment
    ):
        self._font, self._text, self._antialias, self._color, self._bg_color, self._alignment = (
            font if isinstance(font, Font) else self._resolve_font(*font), text, antialias, color, bg_color, alignment
        )
        super().__init__(self._font, self._text, self._antialias, self._color, self._bg_color, self._alignment)

    @property
    def font(self):
        return self._font

    @property
    def text(self):
        return self._text

    @property
    def antialias(self):
        return self._antialias

    @property
    def color(self):
        return self._color

    @property
    def bg_color(self):
        return self._bg_color

    @property
    def alignment(self):
        return self._alignment


class Foreground(Artist[State, SelectedState, ForegroundForm]):
    def __init__(
            self,
            template: Union[ForegroundForm, ForegroundTemplate]
    ):
        super().__init__(template if isinstance(template, ForegroundTemplate) else ForegroundTemplate(*template))
        self._template = cast(ForegroundTemplate, self._template)

    @property
    def size(self):
        return self._template.font.size(self._template.text)

    def draw(self, surface, form: ForegroundForm, component):
        font, text, antialias, color, bg_color, alignment = form
        surface.blit(font.render(text, antialias, color, bg_color), (alignment.offset(surface, text, font), 0))


__all__ = ['LeftAlignment', 'CenterAlignment', 'RightAlignment', 'ForegroundForm', 'ForegroundTemplate', 'Foreground']
