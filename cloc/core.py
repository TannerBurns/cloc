import sys
import re

from colored import fg, style
from typing import Any, Callable, NamedTuple, List, Union

from cloc.utils import defaultattr, trace
from cloc.types import BaseType


class BaseArg(object):
    """BaseArg - Base implementation of an argument found on the cli

       Args:
        name {str} -- used as name for invoking arg
        type {Any} -- A type to use if needed to convert to another type
        help {str} -- help string to describe the base argument

        This class only implements __init__ to set the attributes for the command
    """
    name: str
    type: Any
    help: str

    def __init__(self, name: str, type: Any = None, help: str = None):
        defaultattr(self, 'name', name)
        defaultattr(self, 'type', type)
        defaultattr(self, 'help', help)

class Opt(BaseArg):
    """Opt - Inherits from BaseArg but also adds a short name and default value attribute

       Args:
        short_name {str} -- short name that can also be used to invoke command
        default {Any} -- value to set opt if none is provided
    """
    short_name: str
    default: Any
    multiple: bool
    required: bool

    def __init__(self, name: str, short_name: str, type: Any = None, default: Any= None,
                 multiple: bool= False, required: bool= False, help: str = None):
        super().__init__(name, type, help)
        defaultattr(self, 'short_name', short_name)
        defaultattr(self, 'multiple', multiple)
        defaultattr(self, 'default', default)
        defaultattr(self, 'required', required)

class Flg(BaseArg):
    """Flg - Inherits from BaseArg (very similar to an Opt) but adds a short name and always sets the type to bool

       Args:
        short_name {str} -- short name that can also be used to invoke command
    """
    short_name: str

    def __init__(self, name: str, short_name: str, help: str = None):
        super().__init__(name, bool, help)
        defaultattr(self, 'short_name', short_name)

class Arg(BaseArg):
    """Arg - A copy of BaseArg used for more explicit naming
    """
    def __init__(self, name: str, type: Any = None, help: str = None):
        super().__init__(name, type, help)

class Params(NamedTuple):
    """Params - Inherits from NamedTuple, holds the order of the arg, opt, or flg as they are declared
    """
    order: List[Union[Arg, Opt]]

class BaseCmd(object):
    """BaseCmd - Base implementation of a full command that may or may not include one to many arg, opt, or flg

       Args:
        name {str} -- name used to invoke and track command
        hidden {bool} -- False = Command will be shown; True = Command will not be shown but can be invoked
        help {str} -- help string that will be built to display on --help
        params {Params} -- Params declared by the user [arg, opt, and/or flg]
        regex_patters {list} -- list of regex patterns to match opt and flg against, do not override
        values {list} -- values that are going to be unpacked into the user defined Cmd function

        A BaseCmd cannot be invoked itself. This class must be inherited and completed to correctly run
    """
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
        """_print_help - protected method to print the built help string
            this could in theory be overloaded to also add content to help string before print
        """
        print(self.help)
        sys.exit(0)

    def create_params_regex(self):
        """This is to be implemented by classes that inherit BaseCmd"""
        pass

    def  create_help(self):
        """This is to be implemented by classes that inherit BaseCmd"""
        pass

    def get_params_values(self, cmdl: list):
        """This is to be implemented by classes that inherit BaseCmd"""
        pass

    def _parse(self, cmdl: list):
        """_parse - protected method to initialize the BaseCmd (creates help msg, create param regex patters, and
           get parameter values from the input into parse -> should represent a command line in the state it is in.

           Args:
            cmdl {list} -- the state of the command line
        """
        self.create_help()
        self.create_params_regex()
        self.get_params_values(cmdl)

class Cmd(BaseCmd):
    """Cmd - Inherits from BaseCmd, will implement a start method to invoke the command

       Args:
        fn {Callable} -- the function that got originally decorated
        dataclass {object} -- a Cmd can also become a dataclass Cmd that will allow commands to inherit a self
            attribute which will be added to self.values[0]. This allows commands to become tied to objects to allow
            manipulation of class attributes
    """
    fn: Callable
    dataclass: object

    def __init__(self, name: str, fn: Callable, params: Params = None, hidden: bool = False):
        super().__init__(name, params, hidden)
        self.fn = defaultattr(self, 'fn',  fn)
        self.dataclass = None

    def start(self, cmdl: list):
        """start - This method will invoke the command with the given cmdl state
            cmdl {list} -- the current state of the command line

            1. _parse - call method to initialize command
            2. add dataclass to values if it is a dataclass cmd
            3. call fn with values if exists or fn without args if None

            if self has the attribute of dataclass set, values[0] = dataclass = class that is connected to command
            now command should have a self as first arg or this will override first arg

        """
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
        """new_dataclass_cmd - get a new cls of Cmd that is tied to another class
            name {str} -- name used to invoke and track command
            hidden {bool} -- False = Command will be shown; True = Command will not be shown but can be invoked
            params {Params} -- Params declared by the user [arg, opt, and/or flg]
            dataclass {object} -- new command dataclass = dataclass
        """
        nc = cls(name, fn, params, hidden)
        nc.dataclass = dataclass
        return nc

    def create_help(self):
        """create_help - overloaded from inheritance

           this will iteratively create a help string with
            1. usage
            2. name
            3. docstring
            4. parameters

        """
        namestr = f'\n{fg("green")}{self.name.title()}{style.RESET}\n'
        docstr = f'\n{fg("yellow")}\t{self.__doc__}{style.RESET}\n'
        usagestr = f'\n{fg("blue")}USAGE: {self.name} '
        paramstr = ''
        cmd_tbl = ''
        if getattr(self, 'params'):
            paramstr += f'\n{fg("red")}Parameters:{style.RESET}\n'
            cmd_tbl += f'| {"Name":<18} | {"Short":<8} | {"Type":<16} | {"Help":<54} |\n'
            cmd_tbl += f'| {"-" * 18} | {"-" * 8} | {"-" * 16} | {"-" * 54} |\n'
            for p in self.params.order:
                if isinstance(p, Arg):
                    usagestr += f'{p.name} '
                    cmd_tbl += f'| {p.name:<18} | {" "*8} | {p.type.__name__:<16} | {p.help:<54} |\n'
                if isinstance(p, Opt):
                    usagestr += f'{p.name}|{p.short_name} [value] '
                    cmd_tbl += f'| {p.name:<18} | {p.short_name:<8} | {p.type.__name__:<16} | '
                    attr = 'default'
                    cmd_tbl += f'{"[default: "+str(p.default)+"] "+str(p.help):<54} |\n'
                if isinstance(p,  Flg):
                    usagestr += f'{p.name}|{p.short_name} '
                    cmd_tbl += f'| {p.name:<18} | {p.short_name:<8} | {p.type.__name__:<16} | '
                    cmd_tbl += f'{f"[flag] "+p.help:<54} |\n'

        usagestr += f'{style.RESET}\n'
        self.help = namestr + docstr + usagestr + paramstr + cmd_tbl

    def create_params_regex(self):
        """create_params_regex - create regex patterns for each opt and flg param
            - this allows an easy matching on the entire command line string to opt and flg
            - an empty entry means there was an arg in place, this is indexed for double check later on
        """
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
        """_convert_type - protected method to convert the incoming command line value to the desired  type
            value {Any} - value from command line
            index {int} - index in params order to retrieve type to convert

            check if the type is a builtin and then call builtin on value,
            if custom type is an instance cloc.BaseType then convert the value to the new type
        """
        if 'builtins' == self.params.order[index].type.__class__.__module__:
            value = self.params.order[index].type(value)
        elif isinstance(self.params.order[index].type, BaseType):
            value = self.params.order[index].type.convert(value)
        return value

    def get_params_values(self, cmdl: list):
        """get_params_values - overloaded function, this method will create the values to be unpacked
           into the Cmd function. If --help is anywhere is cmdl, the help message will be printed.
           This helps short circuit if you remember some but not all parameters to a Cmd

            cmdl {list} - command line at current state

        """
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
                        trace(msg, AssertionError, color='red')
                    if cmdl[index]:
                        self.values.append(self._convert_type(cmdl[index], index))
                if isinstance(self.params.order[index], Opt):
                    matches = re.findall(self.regex_patterns[index], ' '.join(cmdl))
                    if matches and len(matches) > 0:
                        if self.params.order[index].multiple:
                            match_list = [m[1] for m in matches]
                            self.values.append(match_list)
                        else:
                            self.values.append(self._convert_type(matches[0][1], index))
                    else:
                        if self.params.order[index].required:
                            msg = f'{self.params.order[index].name!r} is required'
                            trace(msg, AssertionError, color='red')
                        else:
                            if self.params.order[index].default is None:
                                self.values.append(None)
                            else:
                                self.values.append(self._convert_type(self.params.order[index].default, index))
                if isinstance(self.params.order[index], Flg):
                    matches = re.findall(self.regex_patterns[index], ' '.join(cmdl))
                    if matches:
                        self.values.append(True)
                    else:
                        self.values.append(False)

class Grp(BaseCmd):
    """Grp - Inherits from BaseCmd, this class will hold commands and invoked them and modify
       the state of the command line. If a Grp is made with no cmdl supplied then sys.argv[1:] is used,
       grps can pass the cmdl state to another group to chain commands together

       Args:
        commands {List[Cmd]} -- a list of Cmd objects
        invoke {str} -- the string found in command line to invoke a command
        cmdl {list} -- the command line state, if not provided sys.argv[1:] is default

    """
    commands: List[Cmd]
    invoke: str
    cmdl: list

    def __init__(self, name: str, commands: List[Cmd] = None, hidden:bool= False):
        super().__init__(name, hidden=hidden)
        self.commands = defaultattr(self, 'commands', commands or [])

    def __call__(self, cmdl: list= None):
        """__call__ overloading call method to make a Grp hold states and shift the cmdl to another Grp

           Args:
            cmdl {list} -- command line state

            1. call the _parse command from BaseCmd to intialize the group (will update the state of cmdl)
            2. check if an invoke string has been found
            3. if invoke is found, get command that matches the name
            4. if there is a Cmd that matches, check if the instance is a Grp or Cmd
            5. if Grp, call the Cmd with the state of cmdl; if Cmd, call Cmd.start(cmdl) to invoke the command

        """
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
        """add_command - add a new command to the Grp. A command can be either Cmd or Grp. Can also set hidden state

           Args:
            command {BaseCmd} -- a Grp or Cmd to add to current Grp
            hidden {bool} -- flag for hiding Grp or Cmd

            this method will also make a new dataclass Cmd if needed. If a class of commands is given this will
            initiate a dataclass Cmd to be made. Setting dataclass = class that declared the commands.
            This attributes are now tied to this dataclass Cmd to allow a MVC CLI capability
            - this is the magic to allow Cli Viewsets and Querysets
        """
        if not isinstance(command, (Grp, Cmd)):
            # look for groups or commands in this class and make them dataclass commands
            for method_name in dir(command):
                method = getattr(command, method_name)
                if isinstance(method, (Grp, Cmd)):
                    cmd = method.new_dataclass_cmd(method.name, method.fn, method.params, method.hidden, command)
                    cmd.__doc__ = method.__doc__
                    if hidden:
                        cmd.hidden = hidden
                    self.commands.append(cmd)
        else:
            if hidden:
                command.hidden = hidden
            self.commands.append(command)

    def get_command(self, name: str):
        """get_command - find command by name and return the command

           Args:
            name {str} -- name to search
        """
        for c in self.commands:
            if name == c.name:
                return c
        return None

    def get_command_names(self):
        """get_command_names - return all names of commands found in the Grp
        """
        return [c.name for c in self.commands]

    def create_help(self):
        """create_help - overloaded function, this method will create the help message for a Grp

            1. docstring
            2. Usage
            3. list of commands in Grp

        """
        namestr = f'\n{fg("green")}{self.name.title()}{style.RESET}\n'
        docstr = f'\n{fg("yellow")}\t{self.__doc__}{style.RESET}\n'
        usagestr = f'\n{fg("blue")}USAGE: {self.name.upper()} NAME{style.RESET}\n'
        cmdstr = f'\n{fg("red")}Commands:{style.RESET}\n'
        cmd_tbl = f'{fg("red")}| {"Name":<24} | {"Description":<52} |\n'
        cmd_tbl += f'| {"-"*24} | {"-"*52} |\n'
        for c in self.commands:
            cmd_tbl += f'{fg("red")}| {style.RESET}{c.name:<24} {fg("red")}| '
            cmd_tbl += f'{style.RESET}{"".join(str(c.__doc__)[:50]):<52} {fg("red")}|\n'
        cmd_tbl += f'{style.RESET}'
        self.help = namestr + docstr + usagestr + cmdstr + cmd_tbl

    def get_params_values(self, cmdl: list):
        """get_params_values - overloaded function, from the command line state, get the command to invoke and set name

           Args:
            cmdl {list} -- cmdl state

            if nothing is found in command line state or --help is found, print help
            if a command is found, update state of cmdl setting new cmdl = cmdl[1:]
        """
        if len(cmdl) == 0 or (len(cmdl) > 0 and '--help' == cmdl[0]):
            self._print_help()
        if len(cmdl) > 0 and cmdl[0] in self.get_command_names():
            self.invoke = cmdl[0]
            self.cmdl = cmdl[1:]
        else:
            self._print_help()

