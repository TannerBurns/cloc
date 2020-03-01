import os
import re
import json
import io

from datetime import datetime
from typing import Any
from cloc.utils import defaultattr

"""
Types still to make:
    hashtypes - md5, sha1
"""

SHA256_PATTERN = re.compile('[A-Fa-f0-9]{64}')
URL_PATTERN = re.compile('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')

class BaseType(object):
    __name__ = 'cloc.BaseType'
    basetype: Any

    def __init__(self, basetype: Any= None):
        defaultattr(self, 'basetype', basetype)

    def convert(self, value: str):
        """
        overload function for new type cast for param input
        :param value:
        :return:
        """
        return self.basetype(value)

class Choices(BaseType):
    __name__ = 'cloc.Choices'

    def __init__(self, choices:list, basetype: Any = Any):
        super().__init__(basetype)
        self.choices = set(choices)

    def convert(self, value: str):
        if value not in self.choices:
            raise ValueError(f'Error: {value!r} was not found in choices: {", ".join(self.choices)!r}')
        return value

class FileType(BaseType):
    __name__ = 'cloc.File'

    def __init__(self):
        super().__init__(io.TextIOWrapper)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fobj.close()

    def convert(self, filepath: str):
        if not os.path.exists(filepath):
            raise ValueError(f'Error: {filepath!r} does not  exists')
        elif not os.path.isfile(filepath):
            raise ValueError(f'Error: {filepath!r} is not a file')
        self.fobj = open(filepath, 'r')
        return self.fobj

class IntRange(BaseType):
    __name__ = 'cloc.IntRange'
    basetype: int

    def __init__(self, *args):
        super().__init__(int)
        if len(args) == 1:
            self.choices = list(range(args[0]))
        elif len(args) == 2:
            self.choices = list(range(args[0], args[1]))
        else:
            raise ValueError(f'{args!r} was not of length 1 or 2. No start or stop value found.')

    def convert(self, value: str):
        ival =int(value)
        if ival not in self.choices:
            raise ValueError(f'Error:{value!r} -> (int) {ival!r} was not found in choices: {", ".join(self.choices)!r}')
        return ival

class DateType(BaseType):
    __name__ = 'cloc.Date'
    basetype: datetime

    def __init__(self):
        super().__init__(datetime)

    def convert(self, value: str):
        patterns = ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S')
        for p in patterns:
            try:
                return datetime.strptime(value, p)
            except:
                pass
        raise ValueError(f'{value!r} did not match any date patterns: {", ".join(patterns)!r}')

class Sha256Type(BaseType):
    __name__ = 'cloc.Sha256'
    basetype: str

    def __init__(self):
        super().__init__(str)

    def convert(self, value: str):
        if value and isinstance(value, str):
            if os.path.exists(value):
                if os.path.isfile(value):
                    with open(value, 'r') as fin:
                        return SHA256_PATTERN.findall(fin.read())
                else:
                    raise ValueError(f'expected path to be a file, got {value!r}, {type(value).__name__!r}')
            else:
                if SHA256_PATTERN.match(value):
                    return value
                else:
                    raise ValueError(f'{value!r} is not a valid sha256')
        else:
            raise ValueError(f'expected string for sha256 type conversion, got {value!r} of type {type(value).__name__}')

class UrlType(BaseType):
    __name__ = 'cloc.Url'
    basetype: str

    def __init__(self):
        super().__init__(str)

    def convert(self, value: str):
        if URL_PATTERN.match(value):
            return self.basetype(value)
        raise Exception(f'{value!r} is not a valid URL')

class JsonType(BaseType):
    __name__ = 'cloc.Json'
    basetype: dict

    def __init__(self):
        super().__init__(dict)

    def convert(self, value: str):
        try:
            return json.loads(value)
        except:
            raise ValueError(f'{value!r} was not valid JSON')


Url = UrlType()
Json = JsonType()
Sha256 = Sha256Type()
Date = DateType()
File = FileType()