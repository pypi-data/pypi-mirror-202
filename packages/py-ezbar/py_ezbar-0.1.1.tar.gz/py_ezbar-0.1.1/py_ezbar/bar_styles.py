from enum import Enum


class BarStyles(Enum):
    DEFAULT = "default"
    FLAT = "flat"
    LOVE = "love"
    MUSICAL = "musical"


class BarColors(Enum):
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[96m"
    PURPLE = "\033[95m"


BAR_STYLES = {
    "default": {
        "left": "▒",
        "right":  "░",
    },
    "flat": {
        "left": "#",
        "right":  "-",
    },
    "love": {
        "left": "♥",
        "right":  "-",
    },
    "musical": {
        "left": "♪",
        "right":  "-",
    }
}


