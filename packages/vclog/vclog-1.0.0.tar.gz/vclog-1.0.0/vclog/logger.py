from functools import wraps

from .use_cases import Formatter
from .core import Codes


def output(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return_value = function(*args, **kwargs)

        print(return_value)
        if kwargs.get('flush'):
            print(Codes.line_up, end=Codes.line_clear)

    return wrapper


class Logger:
    '''
    The Logger class can be used in two ways: it can be instanced with a name or used as a static class for quick outputs.

    The Logger class has four logging levels: info, debug, warning and error. Moreover it has a plain mode that can be used to log plain text without any prefix.
    '''
    info_prefix: str = Formatter.get('| INFO  |', color='green', bg_color=None, style='bold')
    debug_prefix: str = Formatter.get('| DEBUG |', color='blue', bg_color=None, style='bold')
    warning_prefix: str = Formatter.get('|WARNING|', color='yellow', bg_color=None, style='bold')
    error_prefix: str = Formatter.get('| ERROR |', color='red', bg_color=None, style='bold')

    def __init__(self, name: str) -> None:
        '''
        Parameters
        ----------
        name: str
            the name of the instance
        '''
        self.name: str = name

    @output
    @staticmethod
    def plain(*message, color: str | None = None, bg_color: str | None = None, style: str | list[str] | None = None, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message without any prefix.

        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log

        color: str, optional
            the color of the message. Default to None. Possible values are: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'secondary_black', 'secondary_red', 'secondary_green', 'secondary_yellow', 'secondary_blue', 'secondary_magenta', 'secondary_cyan', 'secondary_white'

        bg_color: str, optional
            the background color of the message. Default to None. Possible values are: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'secondary_black', 'secondary_red', 'secondary_green', 'secondary_yellow', 'secondary_blue', 'secondary_magenta', 'secondary_cyan', 'secondary_white'

        style: str | list[str], optional
            the style of the message. Default to None. Possible values are: 'bold', 'dim', 'italic', 'underline', 'blink', 'highlight', 'hidden', 'strikethrough' and 'double_underline'

        sep: str, optional
            the separation of the given inputs. Default to ''

        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''
        if isinstance(message[0], Logger):
            return Formatter.get(f'[{message[0].name}] {sep.join(map(str, message[1:]))}', color=color, bg_color=bg_color, style=style)
        else:
            return Formatter.get(f'{sep.join(map(str, message))}', color=color, bg_color=bg_color, style=style)

    @output
    @staticmethod
    def info(*message, sep: str = '', flush: bool = False) -> str:
        '''        
        Log the given message at the info level.

        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log

        sep: str, optional
            the separation of the given inputs. Default to ''

        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''
        if isinstance(message[0], Logger):
            return __class__.info_prefix + Formatter.get(f' [{message[0].name}] {sep.join(map(str, message[1:]))}', color='green', bg_color=None, style=None)
        else:
            return __class__.info_prefix + Formatter.get(f' {sep.join(map(str, message))}', color='green', bg_color=None, style=None)

    @output
    @staticmethod
    def debug(*message, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message at the debug level.

        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log

        sep: str, optional
            the separation of the given inputs. Default to ''

        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''
        if isinstance(message[0], Logger):
            return __class__.debug_prefix + Formatter.get(f' [{message[0].name}] {sep.join(map(str, message[1:]))}', color='blue', bg_color=None, style=None)
        else:
            return __class__.debug_prefix + Formatter.get(f' {sep.join(map(str, message))}', color='blue', bg_color=None, style=None)

    @output
    @staticmethod
    def warning(*message, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message at the warning level.

        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log

        sep: str, optional
            the separation of the given inputs. Default to ''

        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''
        if isinstance(message[0], Logger):
            return __class__.warning_prefix + Formatter.get(f' [{message[0].name}] {sep.join(map(str, message[1:]))}', color='yellow', bg_color=None, style=None)
        else:
            return __class__.warning_prefix + Formatter.get(f' {sep.join(map(str, message))}', color='yellow', bg_color=None, style=None)

    @output
    @staticmethod
    def error(*message, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message at the error level.

        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log

        sep: str, optional
            the separation of the given inputs. Default to ''

        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''
        if isinstance(message[0], Logger):
            return __class__.error_prefix + Formatter.get(f' [{message[0].name}] {sep.join(map(str, message[1:]))}', color='red', bg_color=None, style=None)
        else:
            return __class__.error_prefix + Formatter.get(f' {sep.join(map(str, message))}', color='red', bg_color=None, style=None)
