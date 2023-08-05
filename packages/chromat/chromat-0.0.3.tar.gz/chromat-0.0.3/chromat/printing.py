"""
'CHROMAT.printing'
copyright (c) 2023 hex benjamin
full license available at /COPYING
"""

# > IMPORTS
from typing import Literal

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.text import Text

# from rich.table import Table


# > SETUP
chromat_theme = Theme(
    {
        "c.body": "gray42",
        "c.head": "bold gray70",
        "c.title": "reverse bold indian_red",
    },
)

console = Console(theme=chromat_theme)


# > FUNCTIONS
def x3_panel(
    set: tuple[3],
    mode: Literal["rgb", "hsv"] = "rgb",
):
    """Prints RGB values in a table."""

    div = Text(" | ", style="c.head")

    if mode == "rgb":
        title = "RGB"
        styles = ["bold red3", "bold green3", "bold dodger_blue2"]

    if mode == "hsv":
        title = "HSV"
        styles = ["bold deep_pink2", "bold indian_red", "bold gray50"]

    panel = Panel(
        Text(str(set[0]), style=styles[0])
        + div
        + Text(str(set[1]), style=styles[1])
        + div
        + Text(str(set[2]), style=styles[2]),
        title=Text(title, style="italic"),
        title_align="right",
        expand=False,
        padding=(1, 2),
    )

    console.print(panel)
