from enum import StrEnum, auto

ESCSEQ: dict[str, dict[str, str]] = {
    "erase": {"screen": "\u001b[2J"},
    "reset": {
        "all": "\u001b[0m",
        "bold/dim": "\u001b[22m",
        "italic": "\u001b[23m",
        "underline": "\u001b[24m",
        "blink": "\u001b[25m",
        "reverse": "\u001b[27m",
        "invisible ": "\u001b[28m",
        "strikethrough": "\u001b[29m",
        "foreground": "\u001b[39m",
        "background": "\u001b[49m",
        "cursor": "\u001b[H",
    },
    "style": {
        "bold": "\u001b[1m",
        "dim": "\u001b[2m",
        "italic": "\u001b[3m",
        "underline": "\u001b[4m",
        "blink": "\u001b[5m",
        "reverse": "\u001b[7m",
        "invisible ": "\u001b[8m",
        "strikethrough": "\u001b[9m",
    },
    "foreground": {
        "black": "\u001b[30m",
        "red": "\u001b[31m",
        "green": "\u001b[32m",
        "yellow": "\u001b[33m",
        "blue": "\u001b[34m",
        "magenta": "\u001b[35m",
        "cyan": "\u001b[36m",
        "white": "\u001b[37m",
    },
    "background": {
        "black": "\u001b[40m",
        "red": "\u001b[41m",
        "green": "\u001b[42m",
        "yellow": "\u001b[43m",
        "blue": "\u001b[44m",
        "magenta": "\u001b[45m",
        "cyan": "\u001b[46m",
        "white": "\u001b[47m",
    },
}


class Color(StrEnum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()
