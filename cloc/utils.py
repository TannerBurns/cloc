import json

from typing import Any

def defaultattr(cls: object, attribute: str, default: Any= None):
    """defaultattr - check is cls has attribute, if not set default value for attribute, then return attribute

       Args:
        cls {object} -- cls to get or update
        attribute {str} -- attribute name to get or update
        default {Any} -- default value to set if not found

       Return:
        method - attribute from cls
    """
    if not hasattr(cls, attribute):
        setattr(cls, attribute, default)
    return getattr(cls, attribute)

def echoattr(cls: object, attribute: str, list_delimiter: str = '\n', name_only: bool = False, show_type: bool = False):
    """echoattr - print an attribute by name from the cls to stdout

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
                try:
                    msg += json.dumps(value, indent=2)
                except TypeError:
                    msg += str(value)
            elif isinstance(value, (tuple, list)):
                msg += list_delimiter.join((str(v) for v in value))
            else:
                msg += str(value)

        print(msg)
    else:
        print(f'Error: Unable to find attribute with name {attribute!r}')

def listattrs(cls: object, verbose:bool=False):
    """listattrs - list attributes and their values for a cls

       Args:
        cls {object} -- class to list attributes of
    """
    for attr in dir(cls):
        if isinstance(getattr(cls, attr),  (bytes, str, tuple, list, dict)):
            if not verbose and (attr.startswith('__') and attr.endswith('__')):
                continue
            echoattr(cls, attr, list_delimiter=', ')

