from typing import NamedTuple


class Colors(NamedTuple):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    magenta = "\x1b[35m"
    cyan = "\x1b[36m"
    white = "\x1b[37m"

    secondary_black = "\x1b[90m"
    secondary_red = "\x1b[91m"
    secondary_green = "\x1b[92m"
    secondary_yellow = "\x1b[93m"
    secondary_blue = "\x1b[94m"
    secondary_magenta = "\x1b[95m"
    secondary_cyan = "\x1b[96m"
    secondary_white = "\x1b[97m"

    black_bg = "\x1b[40m"
    red_bg = "\x1b[41m"
    green_bg = "\x1b[42m"
    yellow_bg = "\x1b[43m"
    blue_bg = "\x1b[44m"
    magenta_bg = "\x1b[45m"
    cyan_bg = "\x1b[46m"
    white_bg = "\x1b[47m"

    secondary_black_bg = "\x1b[100m"
    secondary_red_bg = "\x1b[101m"
    secondary_green_bg = "\x1b[102m"
    secondary_yellow_bg = "\x1b[103m"
    secondary_blue_bg = "\x1b[104m"
    secondary_magenta_bg = "\x1b[105m"
    secondary_cyan_bg = "\x1b[106m"
    secondary_white_bg = "\x1b[107m"

    @classmethod
    def get(cls, color: str) -> str:
        return getattr(cls, color) if hasattr(cls, color) else ''
