import re
from pathlib import Path
from sys import getsizeof
from typing import Union, Dict, List, Tuple

from PIL import Image


class ImageCache:
    _storage_units: Dict[str, int] = {
        f"{letter}{'i' if base == 2 else ''}b": base ** (power * ordinal)
        for (base, power) in ((2, 10), (10, 3))
        for ordinal, letter in enumerate('kmgtpezy', start=1)
    }
    _size_re = re.compile(
        rf"(\d+)\s*({r'|'.join(r''.join(rf'[{char}{char.upper()}]' for char in key) for key in _storage_units)})"
    )

    @classmethod
    def _parse_size_expr(cls, expr: str):
        matched_str = re.match(cls._size_re, expr)
        if matched_str:
            value, units = matched_str.groups()
            return value * cls._storage_units[units.lower()]

        raise ValueError(f"illegal size expression '{expr}'")

    def __init__(self, size: Union[str, int]):
        self._size = size if type(size) is int else self._parse_size_expr(size)
        self._capacity = self._size
        self._images: Dict[str, Image.Image] = {}
        self._lru: List[Tuple[int, str]] = []

    @property
    def size(self):
        return self._size

    def __getitem__(self, key: Union[str, Path]):
        key = str(key)
        try:
            return self._images[key]
        except KeyError:
            with open(key, 'rb') as fp:
                image = Image.open(fp)
                image.load()

            size = getsizeof(image)
            while self._capacity < size:
                freed_size, freed_key = self._lru.pop()
                self._images.pop(freed_key)
                self._capacity += freed_size

            self._images[key] = image
            self._lru.insert(0, (size, key))
            self._capacity -= size
            return image

    @property
    def storage_use(self):
        return sum(getsizeof(image) for image in self._images.values())

    @property
    def lru_keys(self):
        return set(key for _, key in self._lru)

    @property
    def storage_keys(self):
        return set(self._images)
