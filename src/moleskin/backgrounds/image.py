from os import getenv
from pathlib import Path
from typing import Tuple, Literal, get_args, cast, Union, Generic
import pygame
from PIL.Image import Image
from moleskin.artist import Artist
from moleskin.performance.images import ImageCache
from moleskin.state import State, SelectedState
from moleskin.template import FixedFormTemplate, Template, Form

BackgroundImageForm = Tuple[
    Image
]


class BackgroundImageTemplate(
    FixedFormTemplate[BackgroundImageForm]
):
    _cache_size_varname = 'GAME_BG_IMAGE_CACHE_SIZE'
    _cache = ImageCache(getenv(_cache_size_varname))

    def __init__(self, image_path: Union[str, Path]):
        self._image = self._cache[image_path]
        super().__init__(self._image)


SupportedImageFormat = Literal['P', 'RGB', 'RGBX', 'RGBA', 'ARGB', 'BGRA']


class BackgroundImage(Artist[State, SelectedState, Form], Generic[State, SelectedState, Form]):
    _supported_image_formats: Tuple[SupportedImageFormat, ...] = get_args(SupportedImageFormat)

    @classmethod
    def _cast_image_format(cls, image_format: str) -> SupportedImageFormat:
        if image_format in cls._supported_image_formats:
            return cast(SupportedImageFormat, image_format)

        raise UserWarning(f"unsupported image format {image_format}")

    @classmethod
    def _convert_pil_image(cls, image: Image):
        return pygame.image.frombytes(image.tobytes(), image.size, cls._cast_image_format(image.format))

    def __init__(self, template: Union[str, Image, BackgroundImageTemplate]):
        super().__init__(template if isinstance(template, Template) else BackgroundImageTemplate(template))

    def draw(self, surface, form: BackgroundImageForm, component):
        image, = form
        surface.blit(self._convert_pil_image(image), self._origin)


__all__ = ['BackgroundImage']

