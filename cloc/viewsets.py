import json
import requests

from cloc import mixins, arg, opt, cmd
from cloc.utils import defaultattr
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
        self.queryset = defaultattr(self, 'queryset', GrpQueryset)(*args, **kwargs)
        self.queryset.query(self)


class ReadOnlyViewset(GrpViewset, mixins.Echo, mixins.List, mixins.Version):
    """Read only viewset"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ReqSessionViewset(GrpViewset, mixins.Version):
    """Requests Session Viewset"""
    session: requests.Session
    version: str= '1.0.0'


    def __init__(self, *args, max_retries: int= 3, pool_connections: int= 16,
                 pool_maxsize: int= 16,  raise_exception: bool= True, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool_connections = defaultattr(self, 'pool_connections', pool_connections)
        self.pool_maxsize = defaultattr(self, 'pool_maxsize', pool_maxsize)
        self.max_retries = defaultattr(self, 'max_retries', max_retries)
        self.raise_exception = defaultattr(self, 'raise_exception', raise_exception)
        self.session = requests.Session()
        rqAdapters = requests.adapters.HTTPAdapter(
            pool_connections=self.pool_connections,
            pool_maxsize=self.pool_maxsize,
            max_retries=self.max_retries
        )
        self.session.mount("https://", rqAdapters)
        self.session.mount('http://', rqAdapters)

    def refresh_token(self):
        """Use this to add to verify auth is still valid or refresh if out of date.
        :return:
        """
        pass

    def _make_request(self, request_call, url, **request_kwargs) -> requests.Response:
        """Makes an http request, suppress errors and include content.
        :param session_call: URL the POST request will be made.
        :return: Response
        """
        try:
            response = request_call(url, **request_kwargs)
            if response.status_code == 401:
                self.refresh_token()
            return response
        except Exception as e:
            if self.raise_exception:
                raise
            else:
                response =  requests.Response()
                response.url = url
                response._content = str(e).encode('utf-8')

    @cmd('get')
    @arg('url', type=Url, help='url for get requests')
    @opt('--headers', '-hd', type=Json, help='headers for get request')
    @opt('--params', '-p', type=Json, help='params for get requests')
    @opt('--data', '-d', type=Json, help='data for get requests')
    def get_command(self, url: Url, headers: Json, params: Json, data: Json):
        print(json.dumps(
            self._make_request(self.session.get, url, headers=headers, params=params, data=data).json(), indent=2))








