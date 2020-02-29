import os

from typing import Any
from cloc.utils import defaultattr


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

class FileObj(BaseType):
    __name__ = 'cloc.FileObj'

    def __init__(self, basetype: Any = Any):
        super().__init__(basetype)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fobj.close()

    def convert(self, filepath: str):
        if not os.path.exists(filepath):
            raise ValueError(f'Error: {filepath!r} does not  exists')
        elif not os.path.isfile(filepath):
            raise ValueError(f'Error: {filepath!r} is not a file')
        self.fobj = open(filepath, 'r')
        return self.fobj