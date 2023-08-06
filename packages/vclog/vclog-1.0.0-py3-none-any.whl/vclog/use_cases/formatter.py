from ..core import Codes, Colors


class Formatter:
    @classmethod
    def get(cls, message: str, color: str | None, bg_color: str | None, style: str | list[str] | None) -> str:
        if color is not None:
            message = Colors.get(color) + message + Codes.end

        if bg_color is not None:
            message = Colors.get(bg_color+'_bg') + message + Codes.end

        if style is not None:
            if isinstance(style, str):
                message = Codes.get(style) + message + Codes.end
            else:
                for style_item in style:
                    message = Codes.get(style_item) + message + Codes.end

        return message
