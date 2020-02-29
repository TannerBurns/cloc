import json

from typing import Any

'''
utils
'''
def defaultattr(cls, attribute: str, default: Any= None):
    if not hasattr(cls, attribute):
        setattr(cls, attribute, default)
    return getattr(cls, attribute)

def echoattr(cls, attribute: str, list_delimiter: str = '\n', name_only: bool = False, show_type: bool = False):
    """print an attribute to stdout
    Args:
        attribute {str} -- attribute name
        list_delimiter {str} -- delimiter to join list with [default: '\n']
        show_name {bool} -- option to show attribute name on print
        show_type {bool} -- option to show type of attribute on print
    """
    if hasattr(cls, attribute):
        value = getattr(cls, attribute)

        msg = f'{attribute!r} '

        if not name_only:
            if show_type:
                msg += f'{type(value).__name__!r} '

            if isinstance(value, dict):
                msg += json.dumps(value, indent=2)
            elif isinstance(value, (tuple, list)):
                msg += list_delimiter.join((str(v) for v in value))
            else:
                msg += str(value) if value else ''

        print(msg)
    else:
        print(f'Error: Unable to find attribute with name {attribute!r}')

def listattrs(cls):
    for attr in dir(cls):
        if not attr.startswith('__') and not attr.endswith('__'):
            echoattr(cls, attr, list_delimiter=', ')

