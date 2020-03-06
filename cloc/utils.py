import json
import sys

from colored import fg, style
from typing import Any, Union

def echo(message: Union[str, tuple, list, dict]= None, cls: object= None, attribute: str= None,
             list_delimiter: str = '\n', show_type: bool = False, indent: int= 4, color: str= None):
    """echoattr - print an attribute by name from the cls to stdout

    Args:
        attribute {str} -- attribute name
        list_delimiter {str} -- delimiter to join list with [default: '\n']
        show_name {bool} -- option to show attribute name on print
        show_type {bool} -- option to show type of attribute on print
    """
    msg = ''
    if message:
        if isinstance(message,  str):
            msg += message
        elif isinstance(message, (tuple, list)):
            msg += list_delimiter.join(message)
        elif isinstance(message, dict):
            msg += json.dumps(message, indent=indent)
        else:
            msg += str(message)
    elif cls and attribute:
        if hasattr(cls, attribute):
            value = getattr(cls, attribute)

            msg += f'{attribute!r} '

            if show_type:
                msg += f'{type(value).__name__!r} '

            if isinstance(value, dict):
                try:
                    msg += json.dumps(value, indent=2)
                except TypeError:
                    msg += str(value)
            elif isinstance(value, (tuple, list)):
                msg += list_delimiter.join((str(v) for v in value))
            else:
                msg += str(value)
        else:
            print(f'Error: Unable to find attribute with name {attribute!r} in {cls!r}')
    if color:
        try:
            print(f'{fg(color)}{msg}{style.RESET}')
        except Exception:
            print(msg)
    else:
        print(msg)

def listattrs(cls: object, verbose:bool=False):
    """listattrs - list attributes and their values for a cls

       Args:
        cls {object} -- class to list attributes of
    """
    for attr in dir(cls):
        if isinstance(getattr(cls, attr),  (bytes, str, tuple, list, dict)):
            if not verbose and (attr.startswith('__') and attr.endswith('__')):
                continue
            echo(cls=cls, attribute=attr, list_delimiter=', ')

def trace(message:str, exception: Exception= None, raise_exception: bool= False, exit_code: int= 0, color: str= None):
    if exception and raise_exception:
        if callable(exception):
            exception(message)
    echo(message, color=color)
    sys.exit(exit_code)
