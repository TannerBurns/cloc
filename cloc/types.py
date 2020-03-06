import os
import re
import json
import io

from datetime import datetime
from typing import Any, Union
from cloc.utils import trace

"""
Types still to make:
    hashtypes - md5, sha1
"""

SHA256_PATTERN = re.compile('[A-Fa-f0-9]{64}')
URL_PATTERN = re.compile('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')

class BaseType(object):
    """BaseType - BaseType object for creating new Param types

        convert method should be overloaded to handle value (unpredictable) coming from cmdl state
    """
    __name__ = 'cloc.BaseType'
    basetype: Any

    def __init__(self, basetype: Any= None):
        self.basetype = basetype or str

    def __call__(self, value: str):
        """overload __call__ for converting to new type

        Args:
            value {str} -- value to convert
        """
        return self.basetype(value)

class Choices(BaseType):
    __name__ = 'cloc.Choices'

    def __init__(self, choices:list, basetype: Any = Any):
        super().__init__(basetype)
        self.choices = set(choices)

    def __call__(self, value: str):
        if value not in self.choices:
            trace(f'Error: {value!r} was not found in choices: {", ".join(self.choices)!r}',  TypeError)
        return value

class FileType(BaseType):
    __name__ = 'cloc.File'

    def __init__(self):
        super().__init__(io.TextIOWrapper)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fobj.close()

    def __call__(self, filepath: str):
        if not os.path.exists(filepath):
            trace(f'Error: {filepath!r} does not  exists', TypeError)
        elif not os.path.isfile(filepath):
            trace(f'Error: {filepath!r} is not a file', TypeError)
        self.fobj = open(filepath, 'r')
        return self.fobj

class IntRangeType(BaseType):
    __name__ = 'cloc.IntRange'
    basetype: int

    def __init__(self):
        super().__init__(int)

    def __call__(self, value: Union[str, int]):
        if isinstance(value, str):
            vals = value.split(',')
            if len(vals) == 1:
                return list(range(int(vals[0])))
            elif len(vals) == 2:
                return list(range(int(vals[0]), int(vals[1])))
            else:
                trace(f'Unable to find a start or stop value based on given: {value!r}', TypeError)
        elif isinstance(value, int):
            return list(range(value))
        else:
            trace(f'{value!r} was {type(value).__name__!r} and not {"str"!r} or {"int"!r}', TypeError)

class DateType(BaseType):
    __name__ = 'cloc.Date'
    basetype: datetime

    def __init__(self):
        super().__init__(datetime)

    def __call__(self, value: str):
        patterns = ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S')
        for p in patterns:
            try:
                return datetime.strptime(value, p)
            except:
                pass
        trace(f'{value!r} was {type(value).__name__!r} and not {"str"!r} or {"int"!r}', TypeError)

class Sha256Type(BaseType):
    __name__ = 'cloc.Sha256'
    basetype: str

    def __init__(self):
        super().__init__(str)

    def __call__(self, value: str):
        if value and isinstance(value, str):
            if os.path.exists(value):
                if os.path.isfile(value):
                    with open(value, 'r') as fin:
                        return SHA256_PATTERN.findall(fin.read())
                else:
                    trace(f'expected path to be a file, got {value!r}, {type(value).__name__!r}', TypeError)
            else:
                if SHA256_PATTERN.match(value):
                    return value
                else:
                    trace(f'{value!r} is not a valid sha256', TypeError)
        else:
            trace(f'expected string for sha256 type conversion, got {value!r} of type {type(value).__name__}')

class UrlType(BaseType):
    __name__ = 'cloc.Url'
    basetype: str

    def __init__(self):
        super().__init__(str)

    def __call__(self, value: str):
        if URL_PATTERN.match(value):
            return value
        trace(f'{value!r} is not a valid URL', TypeError)

class JsonType(BaseType):
    __name__ = 'cloc.Json'
    basetype: dict

    def __init__(self):
        super().__init__(dict)

    def __call__(self, value: Union[str, dict]):
        try:
            if isinstance(value, dict):
                return value
            return json.loads(value)
        except:
            trace(f'{value!r} was not valid JSON', TypeError)


"""
Initializing types for users
Choices should be initialized by the user during type set for param
"""
Url = UrlType()
Json = JsonType()
Sha256 = Sha256Type()
Date = DateType()
File = FileType()
IntRange = IntRangeType()