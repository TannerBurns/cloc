
from typing import Any
from cloc.utils import defaultattr


class BaseParamType(object):
    __name__ = 'cloc.BaseParamType'
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

class Choices(BaseParamType):
    __name__ = 'cloc.Choices'

    def __init__(self, choices:list, basetype: Any = Any):
        super().__init__(basetype)
        self.choices = set(choices)

    def convert(self, value: str):
        if value not in self.choices:
            raise ValueError(f'Error: {value!r} was not found in choices: {", ".join(self.choices)!r}')
        return value
