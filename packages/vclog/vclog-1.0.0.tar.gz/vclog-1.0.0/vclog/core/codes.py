from typing import NamedTuple


class Codes(NamedTuple):
    end = "\x1b[0m"
    bold = "\x1b[1m"
    dim = "\x1b[2m"
    italic = "\x1b[3m"
    underline = "\x1b[4m"
    blink = "\x1b[5m"
    highlight = "\x1b[7m"
    hidden = "\x1b[8m"
    strikethrough = "\x1b[9m"
    double_underline = "\x1b[21m"

    line_up = "\x1b[1A"
    line_clear = "\x1b[2K"

    @classmethod
    def get(cls, code: str) -> str:
        return getattr(cls, code) if hasattr(cls, code) else ''
