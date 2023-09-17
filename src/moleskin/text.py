from PIL import Image, ImageDraw2
from PIL.ImageDraw2 import Font

from gui.bases.backgrounds import RGB
from gui.bases.content import Content


class Text(Content):
    def __init__(
            self,
            value: str,
            font: Font,
            color: RGB
    ):
        super().__init__()
        self._value = value
        self._font = font
        self._Color = color
    def rasterize(self, size):
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        ImageDraw2.Draw(image).text((0, 0), self._value, font=self._font)
        return image


__all__ = ['Text']
