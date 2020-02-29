
from typing import Any

from cloc.core import Arg, Cmd, Grp, Opt, Params


'''
decorators
'''
class opt(object):

    def __init__(self, name:str, short_name: str, type: Any= None, help: str= None):
        self.Opt = Opt(name, short_name, type, help)

    def __call__(self, f):
        if isinstance(f, Cmd):
            f.params.order.insert(0, self.Opt)
            return f
        else:
            cmd = Cmd(None, f, params=Params([self.Opt]))
            cmd.__doc__ = f.__doc__
            return cmd

class arg(object):

    def __init__(self, name:str, type: Any= None, help: str= None):
        self.Arg = Arg(name, type, help)

    def __call__(self, f):
        if isinstance(f, Cmd):
            f.params.order.insert(0, self.Arg)
            return f
        else:
            cmd = Cmd(None, f, params=Params([self.Arg]))
            cmd.__doc__ = f.__doc__
            return cmd

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
            c = Cmd(self.name, f, hidden=self.hidden)
            c.__doc__ = f.__doc__
            return c

class grp(object):
    def __init__(self, name:str = None):
        self.name = name

    def __call__(self, f):
        grp = Grp(self.name)
        grp.__doc__ = f.__doc__
        return grp

