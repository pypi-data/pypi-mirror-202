"""
'CHROMAT.swatches'
copyright (c) 2023 hex benjamin
full license available at /COPYING
"""

# > IMPORTS
from .utils import convert_all, hex_to_rgb


# > CLASSES
class Swatch:
    def __init__(
        self,
        rgb_hex: str = None,
        rgb: tuple[int, int, int] = None,
        hsv: tuple[int, int, int] = None,
    ):
        if rgb_hex is not None:
            rgb = hex_to_rgb(rgb_hex)

        if rgb is not None:
            props = convert_all(rgb, "rgb")
        elif hsv is not None:
            props = convert_all(hsv, "hsv")

        for p in props:
            setattr(self, p[0], p[1])

        hex_base = self.rgb.integer
        self.hex = f"#{hex_base[0]:02x}{hex_base[1]:02x}{hex_base[2]:02x}"

    def __repr__(self):
        return f"Swatch({self.hex})"
