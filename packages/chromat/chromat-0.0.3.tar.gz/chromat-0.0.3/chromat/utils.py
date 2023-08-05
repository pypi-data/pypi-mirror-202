"""
'CHROMAT.utils'
copyright (c) 2023 hex benjamin
full license available at /COPYING
"""

# > IMPORTS
from colorsys import hsv_to_rgb, rgb_to_hsv
from typing import Literal, Union


# > FUNCTIONS
def convert_all(color: tuple[int, int, int], mode: Literal["rgb", "hsv"]):
    # --- SETUP ---
    modes = ["rgb", "hsv"]
    in_mode = modes.pop(modes.index(mode))
    out_mode = modes.pop()

    props = []
    components = {
        "rgb": ["red", "green", "blue"],
        "hsv": ["hue", "saturation", "value"],
    }

    if not validate(color, in_mode):
        raise ValueError("Invalid input values for selected mode.")

    # --- INPUT ---
    in_i = color
    in_f = eval(f"{in_mode}_down(*in_i)")

    props.append((in_mode, ChroProp(in_i, in_f)))

    for i, c in enumerate(components[in_mode]):
        props.append((c, ChroProp(in_i[i], in_f[i])))

    # --- CONVERTED ---
    out_f = tuple(
        [round(x, 3) for x in eval(f"{in_mode}_to_{out_mode}(*in_f)")],
    )
    out_i = eval(f"{out_mode}_up(*out_f)")

    props.append((out_mode, ChroProp(out_i, out_f)))

    for i, c in enumerate(components[out_mode]):
        props.append((c, ChroProp(out_i[i], out_f[i])))

    return props


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Converts a string of hex values to RGB.

    Args:
        hex_str (str): The hex string to convert.

    Returns:
        tuple[int, int, int]: A tuple of integer RGB values.
    """
    hex_str = hex_str.strip("#").lower()

    chars = set("0123456789abcdef")
    if any((c not in chars) for c in hex_str):
        return None

    rgb = []
    for i in range(3):
        s = i * 2  # start index
        e = s + 2  # end index
        rgb.append(int(hex_str[s:e], 16))

    return tuple(rgb)


def hsv_down(h, s, v):
    """Scales integer HSV values to floats.

    Args:
        h (int): Hue value, from 0-360.
        s (int): Saturation value, from 0-100.
        v (int): Value value, from 0-100.

    Returns:
        tuple: Scaled HSV values, from 0-1.
    """
    return (round(h / 360, 3), round(s / 100, 3), round(v / 100, 3))


def hsv_up(h, s, v):
    """Scales float HSV values to integers.

    Args:
        h (float): Hue value, from 0-1.
        s (float): Saturation value, from 0-1.
        v (float): Value value, from 0-1.

    Returns:
        tuple: Scaled HSV values, from 0-360, 0-100, and 0-100.
    """
    return (round(h * 360), round(s * 100), round(v * 100))


def rgb_down(r, g, b):
    """Scales integer RGB values to floats.

    Args:
        r (int): Red value, from 0-255.
        g (int): Green value, from 0-255.
        b (int): Blue value, from 0-255.

    Returns:
        tuple: Scaled RGB values, from 0-1.
    """
    return (round(r / 255, 3), round(g / 255, 3), round(b / 255, 3))


def rgb_up(r, g, b):
    """Scales float RGB values to integers.

    Args:
        r (float): Red value, from 0-1.
        g (float): Green value, from 0-1.
        b (float): Blue value, from 0-1.

    Returns:
        tuple: Scaled RGB values, from 0-255.
    """
    return (round(r * 255), round(g * 255), round(b * 255))


def validate(check: tuple[int, int, int], mode: Literal["rgb", "hsv"]) -> bool:
    if mode == "rgb":
        if not all((0 <= x <= 255 for x in check)):
            return False
    elif mode == "hsv":
        if not 0 <= check[:1] <= 360:
            return False
        if not all((0 <= x <= 100 for x in check[1:])):
            return False
    return True


# > CLASSES
class ChroProp:
    def __init__(
        self,
        i_val: Union[int, tuple[int, int, int]],
        f_val: Union[float, tuple[float, float, float]],
    ):
        self.integer = i_val
        self.float = f_val

    def __repr__(self):
        return f"ChroProp([{self.integer}, {self.float}])"
