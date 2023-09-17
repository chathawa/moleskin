from __future__ import annotations
from abc import ABC
from typing import Tuple, Union, Optional, Generic
from pygame import Rect, Color, Surface
from moleskin.artist import Artist, Form, Artists
from moleskin.backgrounds.color import BackgroundColorForm, BackgroundColor, BackgroundColorTemplate
from moleskin.foreground import LeftAlignment, ForegroundForm, ForegroundTemplate, Foreground
from moleskin.layout import Layout, Size, Sizes
from moleskin.state import State, SelectedState
from moleskin.template import Template


class Component(Artist[State, SelectedState, Form], ABC, Generic[State, SelectedState, Form]):
    _default_font = 'dejavusans'
    _default_font_size = 11
    _default_antialias = False
    _default_color = Color(0, 0, 0)
    _default_bg_color = None
    _default_alignment = LeftAlignment()

    def __init__(
            self,
            template: Optional[Template],
            background: Union[str, Color, BackgroundColorForm, BackgroundColor, Template, Artist],
            foreground: Optional[Union[str, ForegroundForm, ForegroundTemplate, Foreground]] = None,
            children: Children = (),
            layout: Layout = None
    ):
        super().__init__(template)
        self._background, self._foreground, self._children, self._layout = (
            background if isinstance(background, Artist) else
            BackgroundColor(
                background if isinstance(background, Template) or type(background) is tuple else
                BackgroundColorTemplate(background)
            ),

            foreground if isinstance(foreground, Foreground) or foreground is None else
            Foreground(
                foreground if isinstance(foreground, Template) or type(foreground) is tuple else
                ForegroundTemplate(
                    (self._default_font, self._default_font_size),
                    foreground,
                    self._default_antialias, self._default_color, self._default_bg_color, self._default_alignment
                )
            ),

            children,
            layout
        )
        self._state: ComponentState = (self._template, self._background, self._foreground, self._children, self._layout)
        self._artists: Artists = (self._background, *self._children, *((self._foreground,) if self._foreground else ()))
        self._current_size = self._foreground.size if self._foreground else (0, 0)
        self._current_artist_subsurfaces: Tuple[Surface, ...] = ()

    def _organized_artists(self, screen: Surface) -> Tuple[
        Size,
        Tuple[Rect, ...]
    ]:
        child_sizes: Sizes = tuple(child._current_size for child in self._children)
        size, child_positions = (
            self._layout.arrange(screen, child_sizes) if self._layout else
            (self._foreground.size, ())
        )
        return size, tuple(Rect(*position, *size) for position, size in zip(
            (self._origin, *child_positions, self._origin),
            (size, *child_sizes, size)
        ))

    def __getstate__(self):
        return self._state

    def __setstate__(self, state: State):
        self.__init__(*state)

    def bind_template(self, state: State, component=None):
        super().bind_template(state, self)

    def draw(self, surface, state: State, component=None):
        if not self._current_artist_subsurfaces:
            self._current_size, self._current_artist_subsurfaces = self._organized_artists(surface)

        for subsurface, artist in zip(self._current_artist_subsurfaces, self._artists):
            artist.draw(surface.subsurface(subsurface), artist.bind_template(state, self), self)

    def on_click(self, x: int, y: int):
        for child_surface, child in zip(self._current_artist_subsurfaces, self._children):
            left, top, right, bottom = child_surface
            if left <= x <= right and bottom <= y <= top:
                return child.on_click(x - left, y - top)


Children = Tuple[
    Component,
    ...
]

ComponentState = Tuple[
    Template,
    Artist,
    Foreground,
    Children,
    Layout
]

__all__ = ['Component']
