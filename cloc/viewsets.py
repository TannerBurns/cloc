
from cloc import mixins
from cloc.utils import defaultattr
from typing import Any, Union

class GrpQueryset(object):
    model: Any

    def __init__(self, model: Any=None):
        self.model = model

    def query(self, cls: object= None):
        """override  by user to query model"""
        pass

class BaseQueryset(GrpQueryset):

    def __init__(self, *args, **kwargs):
        super().__init__(model=kwargs)

    def query(self, cls: object= None):
        if cls:
            obj = cls
        else:
            obj = self
        for key, val in self.model.items():
            setattr(obj, key, val)

class GrpViewset(object):
    version: Union[str, int, float]
    queryset: GrpQueryset

    def __init__(self, *args, **kwargs):
        self.version = defaultattr(self, 'version', None)
        self.queryset = defaultattr(self, 'queryset', None)(*args, **kwargs)
        self.queryset.query(self)


class ReadOnlyViewset(GrpViewset, mixins.Echo, mixins.List, mixins.Version):
    """Read only viewset"""
    queryset = BaseQueryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


