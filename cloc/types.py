
from typing import Any
from cloc.utils import defaultattr


class BaseParamType(object):
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