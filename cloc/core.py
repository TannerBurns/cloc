import sys
import re

from colored import fg, style
from typing import Any, Callable, List, Union

from cloc.utils import trace, echo


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

    def __init__(self, name: str, type: Any = str, help: str = None):
        self.name = name
        self.type = type
        self.help = help


class Arg(BaseArg):
    """Arg - A copy of BaseArg used for more explicit naming
    """

    def __init__(self, name: str, type: Any = None, help: str = None):
        super().__init__(name, type, help)


class Opt(BaseArg):
    """Opt - Inherits from BaseArg but also adds a short name, default, multiple, and required attribute

        short name - an abbreviated shortcut to the cmd
        default - the default value to use if none is given
        multiple - return all instances found in command line instead of first
        require - opt is required in command line for attached Cmd

       Args:
        short_name {str} -- short name that can also be used to invoke command
        default {Any} -- value to set opt if none is provided
    """
    short_name: str
    default: Any
    multiple: bool
    required: bool

    def __init__(self, name: str, short_name: str, type: Any = str, default: Any = None,
                 multiple: bool = False, required: bool = False, help: str = None):
        super().__init__(name, type, help)
        self.short_name = short_name
        self.multiple = multiple
        self.default = default
        self.required = required


class Flg(BaseArg):
    """Flg - Inherits from BaseArg (very similar to an Opt) but adds a short name and always sets the type to bool

       Args:
        short_name {str} -- short name that can also be used to invoke command
    """
    short_name: str

    def __init__(self, name: str, short_name: str, help: str = None):
        super().__init__(name, bool, help)
        self.short_name = short_name


class Params(object):
    """Params - holds the order for parameters given to cmd or grp
    """
    fn: Callable
    order: List[Union[Arg, Opt, Flg]]

    def __init__(self, fn: Callable = None, order: List[Union[Arg, Opt, Flg]] = None):
        """initialize fn and order for Params

           Args:
                fn {Callable} -- function  tied to Parameters
                order {List[Union[Arg, Opt, Flg]]} -- params in order defined
        """
        self.fn = fn
        self.order = order or []

    def get_help(self, name: str) -> tuple:
        """this method for Params will return a tuple of the usage string and parameter table (if exists)

        Args:
            name {str} -- the cmd or grp name calling get_help

        returns tuple(usage, parameter table)
        """
        usage = f'\n{fg("blue")}USAGE: {name} '
        params = ''
        tbl = ''
        if self.order:
            params += f'\n\n{fg("red")}Parameters:{style.RESET}\n'
            tbl += f'| {"Name":<18} | {"Short":<8} | {"Type":<16} | {"Help":<54} |\n'
            tbl += f'| {"-" * 18} | {"-" * 8} | {"-" * 16} | {"-" * 54} |\n'
            for p in self.order:
                if isinstance(p, Arg):
                    usage += f'{p.name} '
                    tbl += f'| {p.name:<18} | {" " * 8} | {p.type.__name__:<16} | {p.help:<54} |\n'
                if isinstance(p, Opt):
                    usage += f'{p.name}|{p.short_name} [value] '
                    tbl += f'| {p.name:<18} | {p.short_name:<8} | {p.type.__name__:<16} | '
                    tbl += f'{"[default: " + str(p.default) + "] " + str(p.help):<54} |\n'
                if isinstance(p, Flg):
                    usage += f'{p.name}|{p.short_name} '
                    tbl += f'| {p.name:<18} | {p.short_name:<8} | {p.type.__name__:<16} | '
                    tbl += f'{f"[flag] " + p.help:<54} |\n'
        usage += f'{style.RESET}'
        return usage, params + tbl


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

    def __init__(self, name: str, params: Params = None, hidden: bool = False):
        self.name = name
        self.params = params
        self.hidden = hidden
        self.help = ''
        self.regex_patterns = []
        self.values = []

    def _print_help(self):
        """_print_help - protected method to print the built help string
            this could in theory be overloaded to also add content to help string before print
        """
        trace(self.help)

    def create_regex_patterns(self):
        """create_regex_patterns - create regex patterns for each opt and flg param
            - this allows an easy matching on the entire command line string to opt and flg
            - an empty entry means there was an arg in place, this is indexed for double check later on
        """
        escape_dash = '\\-'
        if hasattr(self, 'params') and hasattr(self.params, 'order'):
            for p in reversed(self.params.order):
                rgx_pattern = ''
                if isinstance(p, Flg):
                    rgx_pattern += f'(-{f"{escape_dash}"}{p.name.replace("-", "")}|'
                    rgx_pattern += f'-{p.short_name.replace("-", "")})'
                self.regex_patterns.insert(0, rgx_pattern)

    def create_help(self):
        """create_help - a formatted and colored help string, can be overloaded for different formatting

           this will iteratively create a help string with
            1. name
            2. docstring
            3. usage
            4. parameters

        """
        name = f'\n{fg("green")}{self.name.title()}{style.RESET}\n'
        doc = f'\n{fg("yellow")}\t{self.__doc__}{style.RESET}\n'
        usage, params = self.params.get_help(self.name)
        self.help = name + doc + usage + params

    def get_values(self, cmdl: list):
        """This is to be implemented by classes that inherit BaseCmd"""
        pass

    def _parse(self, cmdl: list):
        """_parse - protected method to initialize the BaseCmd (creates help msg, create param regex patters, and
           get parameter values from the input into parse -> should represent the latest state of the command line.

           Args:
            cmdl {list} -- the state of the command line
        """
        self.create_help()
        self.create_regex_patterns()
        self.get_values(cmdl)


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
        self.fn = fn
        self.dataclass = None
        self.__doc__ = fn.__doc__

    def __call__(self, cmdl: list = None):
        """This method will invoke the command with the given cmdl state

           Args:
            cmdl {list} -- the current state of the command line

            1. _parse - call method to initialize command
            2. add dataclass to values if it is a dataclass cmd
            3. call fn with values if exists or fn without args if None

            if self has the attribute of dataclass set, values[0] = dataclass = class that is connected to command
            now command should have a self as first arg or this will override first arg

        """
        self._parse(cmdl or sys.argv[1:])

        # this should represent 'self' for the command about to start
        if self.dataclass:
            self.values.insert(0, self.dataclass)

        return self.fn(*self.values) if self.values else self.fn()

    @classmethod
    def create_new_cmd(cls, name: str, fn: Callable, params: Params = None,
                       hidden: bool = False):
        return cls(name, fn, params=params, hidden=hidden)

    @classmethod
    def create_new_dataclass_cmd(cls, name: str, fn: Callable, params: Params = None,
                                 hidden: bool = False, dataclass: object = None):
        """create_new_dataclass_cmd - get a new cls of Cmd that is tied to another class

           Args:
            name {str} -- name used to invoke and track command
            hidden {bool} -- False = Command will be shown; True = Command will not be shown but can be invoked
            params {Params} -- Params declared by the user [arg, opt, and/or flg]
            dataclass {object} -- new command dataclass = dataclass
        """
        new_cmd = cls(name, fn, params, hidden)
        new_cmd.dataclass = dataclass
        return new_cmd

    def get_values(self, cmdl: list):
        """get_values - overloaded function, this method will create the values to be unpacked
           into the Cmd function. If --help is anywhere is cmdl, the help message will be printed.

           Args:
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
                    if len(cmdl) >= index + 1 and cmdl[index + 1]:
                        self.values.append(self.params.order[index].type(cmdl[index + 1]))
                if isinstance(self.params.order[index], Opt):
                    values = []
                    for cmdl_index in range(0, len(cmdl)):
                        if cmdl[cmdl_index] == self.params.order[index].name or \
                                cmdl[cmdl_index] == self.params.order[index].short_name:
                            if len(cmdl) >= cmdl_index + 1 and cmdl[cmdl_index + 1]:
                                values.append(self.params.order[index].type(cmdl[cmdl_index + 1]))

                    if self.params.order[index].required and not values:
                        msg = f'{self.params.order[index].name!r} is required'
                        trace(msg, AssertionError, color='red')

                    if len(values) > 0:
                        if self.params.order[index].multiple:
                            self.values.append(values)
                        else:
                            self.values.append(values[0])
                    elif self.params.order[index].default is None:
                        self.values.append(self.params.order[index].default)
                    elif self.params.order[index].default:
                        self.values.append(self.params.order[index].type(self.params.order[index].default))
                if isinstance(self.params.order[index], Flg):
                    matches = re.findall(self.regex_patterns[index], ' '.join(cmdl))
                    self.values.append(True) if matches else self.values.append(False)


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
    cmdl: list
    fn: Callable
    params: Params
    dataclass: object
    invoke: str  # this is here in the case you want to manually set a cmd to call in self.commands

    def __init__(self, name: str, fn: Callable, commands: List[Cmd] = None, params: Params = None,
                 hidden: bool = False):
        super().__init__(name, params=params, hidden=hidden)
        self.commands = commands or []
        self.fn = fn
        self.params = params
        self.__doc__ = fn.__doc__
        self.invoke = ''

    def __call__(self, cmdl: list = None):
        """__call__ overloading call method to make a Grp hold states and shift the cmdl to another Grp

           Args:
            cmdl {list} -- command line state

            1. call the _parse command from BaseCmd to intialize the group (will update the state of cmdl)
            2. check if an invoke string has been found
            3. if invoke is found, get command that matches the name
            4. if there is a Cmd that matches, check if the instance is a Grp or Cmd
            5. if Grp, call the Cmd with the state of cmdl; if Cmd, call Cmd.start(cmdl) to invoke the command

        """
        # need to rework to also call grp function to chain both and allow grp to have opt and flg
        self.cmdl = cmdl or sys.argv[1:]
        self._parse(self.cmdl)
        self.fn(*self.values)

        # check if command was found to invoke
        if self.invoke:
            cmd = self.get_command(self.invoke)
            if cmd:
                cmd(self.cmdl)
            else:
                echo(f'command {self.invoke!r} was not found', color='red')
                self._print_help()
        else:
            self._print_help()

    def add_command(self, command: BaseCmd, hidden: bool = None):
        """add_command - add a new command to the Grp. A command can either be a Cmd or Grp.
            Can also override or set hidden state

           Args:
            command {BaseCmd} -- a Grp or Cmd to add to current Grp
            hidden {bool} -- flag for hiding Grp or Cmd

            this method will also make a new dataclass Cmd if needed. If a command is found inside a class,
            initiate a dataclass Cmd to be made. Setting dataclass = class that declared the commands.
            This attributes are now tied to this dataclass Cmd to allow a MVC CLI capability
            - a dataclass Cmd is the magic to allow Cli Viewsets and Querysets
        """
        if not isinstance(command, (Grp, Cmd)):
            # look for groups or commands in this class and make them dataclass commands
            for method_name in dir(command):
                method = getattr(command, method_name)
                if isinstance(method, Cmd):
                    cmd = method.create_new_dataclass_cmd(method.name, method.fn, method.params, method.hidden, command)
                    if cmd:
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
        doc = f'\n{fg("yellow")}\t{self.__doc__}{style.RESET}\n'
        cmdstr = ''
        grp_tbl = ''
        usage, params = self.params.get_help(self.name)
        if self.commands:
            cmdstr += f'\n\n{fg("red")}Commands:{style.RESET}\n' if self.commands else ''
            grp_tbl += f'{fg("red")}| {"Name":<24} | {"Description":<52} |\n'
            grp_tbl += f'| {"-" * 24} | {"-" * 52} |\n'
            for c in self.commands:
                grp_tbl += f'{fg("red")}| {style.RESET}{c.name:<24} {fg("red")}| '
                grp_tbl += f'{style.RESET}{"".join(str(c.__doc__)[:50]):<52} {fg("red")}|\n'
            grp_tbl += f'{style.RESET}'
        usage = usage + ' ' + '|'.join(self.get_command_names())
        self.help = namestr + doc + usage + params + cmdstr + grp_tbl

    def get_values(self, cmdl: list):
        """get_values - overloaded function, from the command line state, get the command to invoke and set name

           Args:
            cmdl {list} -- cmdl state

        """

        cur_state = []
        cmd_names = self.get_command_names()
        for index in range(0, len(cmdl)):
            if cmdl[index] in cmd_names:
                cur_state = cmdl[:index]
                self.invoke = cmdl[index]
                self.cmdl = cmdl[index:]
                break
        if '--help' in cur_state or (len(cur_state) == 0 and all('--help' in c for c in self.cmdl)):
            self._print_help()
        if not self.invoke:
            cur_state = self.cmdl
        if hasattr(self, 'params') and hasattr(self.params, 'order'):
            while len(cur_state) < len(self.params.order):
                cur_state.append('')
            for index in range(0, len(self.params.order)):
                if isinstance(self.params.order[index], Arg):
                    if cur_state[index].startswith('-'):
                        msg = f'An {"opt"!r} was found: {cur_state[index]!r}, '
                        msg += f'instead of type {"arg"!r}. Order of cmd parameters might be incorrect.'
                        trace(msg, AssertionError, color='red')
                    if cur_state[index]:
                        self.values.append(self.params.order[index].type(cur_state[index]))
                if isinstance(self.params.order[index], Opt):
                    values = []
                    for cmdl_index in range(0, len(cmdl)):
                        if cmdl[cmdl_index] == self.params.order[index].name or \
                                cmdl[cmdl_index] == self.params.order[index].short_name:
                            if len(cmdl) >= cmdl_index + 1 and cmdl[cmdl_index + 1]:
                                values.append(self.params.order[index].type(cmdl[cmdl_index + 1]))

                    if self.params.order[index].required and not values:
                        msg = f'{self.params.order[index].name!r} is required'
                        trace(msg, AssertionError, color='red')

                    if len(values) > 0:
                        if self.params.order[index].multiple:
                            self.values.append(values)
                        else:
                            self.values.append(values[0])
                    elif self.params.order[index].default is None:
                        self.values.append(self.params.order[index].default)
                    elif self.params.order[index].default:
                        self.values.append(self.params.order[index].type(self.params.order[index].default))
                if isinstance(self.params.order[index], Flg):
                    matches = re.findall(self.regex_patterns[index], ' '.join(cur_state))
                    self.values.append(True) if matches else self.values.append(False)

    @classmethod
    def create_new_grp(cls, name: str, fn: Callable, commands: List[Cmd] = None,
                       params: Params = None, hidden: bool = False):
        return cls(name, fn, commands=commands, params=params, hidden=hidden)