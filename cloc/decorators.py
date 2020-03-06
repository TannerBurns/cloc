import inspect
from typing import Any

from cloc.core import Arg, Cmd, Grp, Opt, Flg, Params


class opt(object):
    """opt - decorator for creating a new Opt parameter

       Args:
        name {str} -- name for opt ex: --opt1
        short_name {str} -- short name for opt ex: -o1
        type {Any} -- type for opt ex: str
        default {Any} -- default value for opt if opt is not provided
        help {str} -- help string for opt
    """

    def __init__(self, name:str, short_name: str, type: Any= None, default: Any= None,
                 multiple:bool= False, required: bool= False, help: str= None):
        self.Opt = Opt(name, short_name, type, default, multiple, required, help)

    def __call__(self, f):
        if isinstance(f, Params):
            f.order.insert(0, self.Opt)
            return f
        else:
            return Params(fn=f, order=[self.Opt])

class flg(object):
    """flg - decorator for creating a new Flg parameter

       Args:
        name {str} -- name for opt ex: --flg1
        short_name {str} -- short name for opt ex: -f1
        help {str} -- help string for flg
    """
    def __init__(self, name:str, short_name: str, help: str= None):
        self.Flg = Flg(name, short_name, help)

    def __call__(self, f):
        if isinstance(f, Params):
            f.order.insert(0, self.Flg)
            return f
        else:
            return Params(fn=f, order=[self.Flg])

class arg(object):
    """arg - decorator for creating a new Arg parameter

       Args:
        name {str} -- name for opt ex: arg1
        type {Any} -- type for opt ex: str
        help {str} -- help string for arg
    """
    def __init__(self, name:str, type: Any= None, help: str= None):
        self.Arg = Arg(name, type, help)

    def __call__(self, f):
        if isinstance(f, Params):
            f.order.insert(0, self.Arg)
            return f
        else:
            return Params(fn=f, order=[self.Arg])

class cmd(object):
    """cmd - decorator for creating a new Cmd

       Args:
        name {str} -- name to give Cmd
        hidden {bool} -- flag for Cmd to be hidden
    """
    def __init__(self, name:str = None, hidden:bool = False):
        self.name = name
        self.hidden = hidden

    def __call__(self, f):
        if isinstance(f, Cmd):
            return f
        elif isinstance(f, Params):
            return Cmd.create_new_cmd(self.name, f.fn, params=f, hidden=self.hidden)
        else:
            return Cmd.create_new_cmd(self.name, f, params=Params(fn=f), hidden=self.hidden)

class grp(object):
    """grp - decorator for creating a new Grp

       Args:
        name {str} -- name to give Grp
        hidden {bool} -- flag for Grp to be hidden
    """
    def __init__(self, name:str = None, hidden:bool = False):
        self.name = name
        self.hidden  = hidden

    def __call__(self, f):
        if isinstance(f, Grp):
            return f
        elif isinstance(f, Params):
            return Grp.create_new_grp(self.name, f.fn, params=f, hidden=self.hidden)
        else:
            return Grp.create_new_grp(self.name, f, params=Params(fn=f), hidden=self.hidden)

