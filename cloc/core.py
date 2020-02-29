import sys
import re
import inspect

from typing import Any, Callable, NamedTuple, List, Union

from cloc.utils import defaultattr
from cloc.types import BaseType

'''
core
'''
class BaseArg(object):
    name: str
    type: Any
    help: str

    def __init__(self, name: str, type: Any = None, help: str = None):
        defaultattr(self, 'name', name)
        defaultattr(self, 'type', type)
        defaultattr(self, 'help', help)

class Opt(BaseArg):
    short_name: str

    def __init__(self, name: str, short_name: str, type: Any = None, help: str = None):
        super().__init__(name, type, help)
        defaultattr(self, 'short_name', short_name)

class Flg(BaseArg):
    short_name: str

    def __init__(self, name: str, short_name: str, help: str = None):
        super().__init__(name, bool, help)
        defaultattr(self, 'short_name', short_name)

class Arg(BaseArg):

    def __init__(self, name: str, type: Any = None, help: str = None):
        super().__init__(name, type, help)

class Params(NamedTuple):
    order: List[Union[Arg, Opt]]

class BaseCmd(object):
    name: str
    hidden: bool
    help: str
    params: Params
    regex_patterns: list
    values: list

    def __init__(self, name: str, params: Params = None, hidden: bool= False):
        self.name = defaultattr(self, 'name', name)
        self.params = defaultattr(self, 'params', params)
        self.hidden = defaultattr(self, 'hidden', hidden)
        self.help = ''
        self.regex_patterns = []
        self.values = []

    def _print_help(self):
        print(self.help)
        sys.exit(0)

    def create_params_regex(self):
        """Cmd will inherit this for overloading, Grp will inherit with pass"""
        pass

    def  create_help(self):
        """will be overloaded"""
        pass

    def get_params_values(self, cmdl: list):
        """will be overloaded"""
        pass

    def _parse(self, cmdl: list):
        self.create_help()
        self.create_params_regex()
        self.get_params_values(cmdl)

class Cmd(BaseCmd):
    fn: Callable
    dataclass: object

    def __init__(self, name: str, fn: Callable, params: Params = None, hidden: bool = False):
        super().__init__(name, params, hidden)
        self.fn = defaultattr(self, 'fn',  fn)
        self.dataclass = None

    def start(self, cmdl: list):
        self._parse(cmdl)

        # this should represent 'self' for the command about to start
        if self.dataclass:
            self.values.insert(0, self.dataclass)

        if self.values:
            self.fn(*self.values)
        else:
            self.fn()

    @classmethod
    def new_dataclass_cmd(cls, name: str, fn: Callable, params: Params= None, hidden: bool= False, dataclass= None):
        nc = cls(name, fn, params, hidden)
        nc.dataclass = dataclass
        return nc

    def create_help(self):
        docstr = f'\n{self.__doc__}\n\n'
        usagestr = f'\nUSAGE: {self.name} '
        paramstr = f'Parameters\n{"="*80}\n'
        if getattr(self, 'params'):
            for p in self.params.order:
                if isinstance(p, Arg):
                    usagestr += f'{p.name} '
                    paramstr += f'{type(p).__name__!r} '
                    if p.type:
                        paramstr += f'\t{p.type.__name__!r} '
                    paramstr += f'\t{p.name} '
                    if p.help:
                        paramstr += f'\t{p.help} '
                    paramstr += '\n'
                if isinstance(p, Opt):
                    usagestr += f'{p.name}|{p.short_name} [value] '
                    paramstr += f'{type(p).__name__!r} '
                    if p.type:
                        paramstr += f'\t{p.type.__name__!r} '
                    paramstr += f'\t{p.name} {p.short_name} '
                    if p.help:
                        paramstr += f'\t{p.help} '
                    paramstr += '\n'
                if isinstance(p,  Flg):
                    usagestr += f'{p.name}|{p.short_name} '
                    paramstr += f'{type(p).__name__!r} '
                    if p.type:
                        paramstr += f'\t{p.type.__name__!r} (flag) '
                    paramstr += f'\t{p.name} {p.short_name} '
                    if p.help:
                        paramstr += f'\t{p.help} '
                    paramstr += '\n'

        usagestr += '\n'
        self.help = usagestr + docstr + paramstr

    def create_params_regex(self):
        escape_dash = '\\-'
        if hasattr(self, 'params'):
            if hasattr(self.params, 'order'):
                for p in reversed(self.params.order):
                    rgx_pattern = ''
                    if isinstance(p, Opt):
                        rgx_pattern += f'(-{f"{escape_dash}"}{p.name.replace("-", "")}|'
                        rgx_pattern += f'-{p.short_name.replace("-", "")}) ([\S]*)'
                    elif isinstance(p, Flg):
                        rgx_pattern += f'(-{f"{escape_dash}"}{p.name.replace("-", "")}|'
                        rgx_pattern += f'-{p.short_name.replace("-", "")})'
                    self.regex_patterns.insert(0, rgx_pattern)


    def _convert_type(self, value: Any, index: int):
        if 'builtins' == self.params.order[index].type.__class__.__module__:
            value = self.params.order[index].type(value)
        elif isinstance(self.params.order[index].type, BaseType):
            value = self.params.order[index].type.convert(value)
        return value

    def get_params_values(self, cmdl: list):
        if '--help' in cmdl:
            self._print_help()
        if hasattr(self, 'params') and hasattr(self.params, 'order'):
            while len(cmdl) < len(self.params.order):
                cmdl.append('')
            for index in range(0, len(self.params.order)):
                if isinstance(self.params.order[index], Arg):
                    if cmdl[index].startswith('-'):
                        msg = f'An {"opt"!r} was found: {cmdl[index]!r}, '
                        msg += f'instead of type {"arg"!r}. Order of cmd parameters might be incorrect.'
                        raise TypeError(msg)
                    if cmdl[index]:
                        self.values.append(self._convert_type(cmdl[index], index))
                if isinstance(self.params.order[index], Opt):
                    matches = re.findall(self.regex_patterns[index], ' '.join(cmdl))
                    if matches:
                        for m in matches:
                            if m[1]:
                                self.values.append(self._convert_type(m[1], index))
                if isinstance(self.params.order[index], Flg):
                    matches = re.findall(self.regex_patterns[index], ' '.join(cmdl))
                    if matches:
                        self.values.append(True)

class Grp(BaseCmd):
    commands: List[Cmd]
    invoke: str
    cmdl: list

    def __init__(self, name: str, commands: List[Cmd] = None, hidden:bool= False):
        super().__init__(name, hidden=hidden)
        self.commands = defaultattr(self, 'commands', commands or [])

    def __call__(self, cmdl: list= None):
        self.cmdl = cmdl or sys.argv[1:]
        self._parse(self.cmdl)
        if self.invoke:
            cmd = self.get_command(self.invoke)
            if cmd:
                if isinstance(cmd, Grp):
                    cmd(self.cmdl)
                if isinstance(cmd, Cmd):
                    cmd.start(self.cmdl)
        else:
            self._print_help()

    def add_command(self, command: BaseCmd, hidden:bool= None):
        if not isinstance(command, (Grp, Cmd)):
            # look for groups or commands in this class and make them dataclass commands
            for method_name in dir(command):
                method = getattr(command, method_name)
                if isinstance(method, (Grp, Cmd)):
                    cmd = method.new_dataclass_cmd(method.name, method.fn, method.params, method.hidden, command)
                    if hidden:
                        cmd.hidden = hidden
                    self.commands.append(cmd)
        else:
            if hidden:
                command.hidden = hidden
            self.commands.append(command)

    def get_command(self, name: str):
        for c in self.commands:
            if name == c.name:
                return c
        return None

    def get_command_names(self):
        return [c.name for c in self.commands]

    def create_help(self):
        docstr = f'\n{self.__doc__}\n\n'
        usagestr = '\nUSAGE: COMMAND [Arg|Opt] ...\n'
        cmdstr = f'Commands:\n{"="*80}\n'
        if hasattr(self, 'commands'):
            for c in self.commands:
                if not c.hidden:
                    cmdstr += f'{c.name}\n'
        self.help = usagestr + docstr + cmdstr

    def get_params_values(self, cmdl: list):
        if len(cmdl) == 0 or (len(cmdl) > 0 and '--help' == cmdl[0]):
            self._print_help()
        if len(cmdl) > 0 and cmdl[0] in self.get_command_names():
            self.invoke = cmdl[0]
            self.cmdl = cmdl[1:]
        else:
            self._print_help()

