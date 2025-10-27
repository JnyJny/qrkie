""" """

from enum import Enum
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer,
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)


class Style(str, Enum):
    square: str = "square"
    rounded: str = "rounded"
    circle: str = "circle"
    gapped: str = "gapped"
    vertical: str = "vertical"
    horizontal: str = "horizontal"

    @property
    def drawer(self):
        match self.value:
            case "square":
                return SquareModuleDrawer()
            case "rounded":
                return RoundedModuleDrawer()
            case "circle":
                return CircleModuleDrawer()
            case "gapped":
                return GappedSquareModuleDrawer()
            case "vertical":
                return VerticalBarsDrawer()
            case "horizontal":
                return HorizontalBarsDrawer()
            case _:
                raise ValueError(f"Unknown style: {self.value}")
