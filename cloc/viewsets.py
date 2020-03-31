import json
import requests

from cloc import mixins, arg, opt, cmd
from cloc.utils import echo
from cloc.types import Url, Json

from typing import Any, Union

class BaseQueryset(object):
    model: Any

    def __init__(self, model: Any=None):
        self.model = model

    def query(self, cls: object= None):
        """override  by user to query model"""
        pass

class GrpQueryset(BaseQueryset):

    def __init__(self, *args, **kwargs):
        super().__init__(model=kwargs)

    def query(self, cls: object= None):
        obj = cls or self
        for key, val in self.model.items():
            setattr(obj, key, val)

class GrpViewset(object):
    version: Union[str, int, float]
    queryset: GrpQueryset

    def __init__(self, *args, **kwargs):
        self.version = kwargs.pop('version', None)
        self.queryset = kwargs.pop('queryset', GrpQueryset)(*args, **kwargs)
        self.queryset.query(self)


class ReadOnlyViewset(GrpViewset, mixins.Echo, mixins.List, mixins.Version):
    """Read only viewset"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ReqSessionViewset(GrpViewset, mixins.Version):
    """Requests Session Viewset"""
    session: requests.Session
    version: str= '1.0.0'


    def __init__(self, *args, session: requests.Session= None ,max_retries: int= 3,
                 pool_connections: int= 16, pool_maxsize: int= 16,  raise_exception: bool= True, **kwargs):
        super().__init__(*args, **kwargs)
        if session:
            self.session = session
        else:
            self.pool_connections = pool_connections
            self.pool_maxsize = pool_maxsize
            self.max_retries = max_retries
            self.raise_exception = raise_exception
            self.session = requests.Session()
            session_adapters = requests.adapters.HTTPAdapter(
                pool_connections=self.pool_connections,
                pool_maxsize=self.pool_maxsize,
                max_retries=self.max_retries
            )
            self.session.mount("https://", session_adapters)
            self.session.mount('http://', session_adapters)

    @cmd('get')
    @arg('url', type=Url, help='url for get requests')
    @opt('--headers', '-hd', type=Json, default={}, help='headers for get request')
    @opt('--params', '-p', type=Json, default={}, help='params for get requests')
    @opt('--data', '-d', type=Json, default={}, help='data for get requests')
    def get_command(self, url: Url, headers: Json, params: Json, data: Json):
        """session get requests"""
        echo(self.session.get(url, headers=headers, params=params, data=data).json())








