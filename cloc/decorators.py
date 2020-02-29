
from typing import Any, Callable, Union

from cloc.core import Arg, Cmd, Grp, Opt, Flg, Params


'''
decorators
'''

def _create_cmd(name:str, fn:Callable, param:Union[Arg, Flg, Opt], hidden:bool=False):
    if param:
        cmd = Cmd(name, fn, params=Params([param]), hidden=hidden)
    else:
        cmd = Cmd(name, fn, hidden=hidden)
    cmd.__doc__ = fn.__doc__
    return cmd

class opt(object):

    def __init__(self, name:str, short_name: str, type: Any= None, help: str= None):
        self.Opt = Opt(name, short_name, type, help)

    def __call__(self, f):
        if isinstance(f, Cmd):
            f.params.order.insert(0, self.Opt)
            return f
        else:
            return _create_cmd(None, f, self.Opt)

class flg(object):

    def __init__(self, name:str, short_name: str, help: str= None):
        self.Flg = Flg(name, short_name, help)

    def __call__(self, f):
        if isinstance(f, Cmd):
            f.params.order.insert(0, self.Flg)
            return f
        else:
            return _create_cmd(None, f, self.Flg)

class arg(object):

    def __init__(self, name:str, type: Any= None, help: str= None):
        self.Arg = Arg(name, type, help)

    def __call__(self, f):
        if isinstance(f, Cmd):
            f.params.order.insert(0, self.Arg)
            return f
        else:
            return _create_cmd(None, f, self.Arg)

class cmd(object):

    def __init__(self, name:str = None, hidden:bool = False):
        self.name = name
        self.hidden = hidden

    def __call__(self, f):
        if isinstance(f, Cmd):
            f.name = self.name
            f.hidden = self.hidden
            return f
        else:
            return _create_cmd(self.name, f, None, hidden=self.hidden)

class grp(object):
    def __init__(self, name:str = None, hidden:bool = False):
        self.name = name
        self.hidden  = hidden

    def __call__(self, f):
        grp = Grp(self.name, hidden=self.hidden)
        grp.__doc__ = f.__doc__
        return grp

