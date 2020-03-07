# cloc

<!--Badges-->
![MIT badge](https://img.shields.io/badge/license-MIT-black)
![Python3.6 badge](https://img.shields.io/badge/python-v3.6+-blue?logo=python&logoColor=yellow)
![Platform badge](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win32-yellow)

### Command Line Object Chaining

    Command line framework for making simple and complex command line applications.
    
* Easily create stand alone commands or nested groups of commands
* Define and connect commands with class objects
* Inherit and create viewsets of commands to be able to reuse large nested groups in other cli applications
* Use mixin commands to quickly add pre defined commands to your cli
* Groups of commands can be found from any class that has defined a `cloc.core.BaseCmd`

- [ Installation ](#install)
- [ Documentation ](#docs)
    - [ Cmd and Grp ](#cmd_and_grp)
    - [ Parameters - Arg, Opt, and Flg ](#parameters)
    - [ Classes ](#classes)
        - [ cloc.core.BaseCmd ](#cloc_basecmd)
            - [ BaseCmd.values ](#cloc_basecmd_values)
            - [ BaseCmd.params ](#cloc_basecmd_params)
            - [ BaseCmd._parse ](#cloc_basecmd__parse)
            - [ BaseCmd.create_help ](#cloc_basecmd_create_help)
            - [ BaseCmd._print_help ](#cloc_basecmd__print_help)
            - [ BaseCmd.create_regex_patterns ](#cloc_basecmd_create_regex_patterns)
            - [ BaseCmd.get_values ](#cloc_basecmd_get_values)
        - [ cloc.core.Cmd ](#cloc_cmd)
            - [ Cmd.fn ](#cloc_cmd_fn)
            - [ Cmd.dataclass ](#cloc_cmd_dataclass)
            - [ Cmd.new_dataclass_cmd ](#cloc_cmd_new_dataclass_cmd)
            - [ Cmd.create_regex_patterns ](#cloc_cmd_create_regex_patterns)
            - [ Cmd.get_values ](#cloc_cmd_get_values)
        - [ cloc.core.Grp ](#cloc_grp)
            - [ Grp.commands ](#cloc_grp_commands)
            - [ Grp.invoke ](#cloc_grp_invoke)
            - [ Grp.cmdl ](#cloc_grp_cmdl)
            - [ Grp.add_command ](#cloc_grp_add_command)
            - [ Grp.get_command ](#cloc_grp_get_command)
    - [ Decorators ](#decorators)
        - [ cloc.decorators.cmd ](#decorators_cmd)
        - [ cloc.decorators.grp ](#decorators_grp)
        - [ cloc.decorators.arg ](#decorators_arg)
        - [ cloc.decorators.opt ](#decorators_opt)
        - [ cloc.decorators.flg ](#decorators_flg)
    - [ Types ](#cloc.types_2119495137)
        - [ cloc.types.BaseType ](#cloc.types.BaseType_1669657826)
            - [ BaseType.__call__ ](#BaseType.__call___1591412620)
        - [ cloc.types.Choices ](#cloc.types.Choices_1347752155)
        - [ cloc.types.DateType ](#cloc.types.DateType_974986765)
        - [ cloc.types.FileType ](#cloc.types.FileType_442405428)
            - [ FileType.__exit__ ](#FileType.__exit___1883566034)
        - [ cloc.types.IntRangeType ](#cloc.types.IntRangeType_483716711)
        - [ cloc.types.JsonType ](#cloc.types.JsonType_806135893)
        - [ cloc.types.Sha256Type ](#cloc.types.Sha256Type_897860609)
        - [ cloc.types.UrlType ](#cloc.types.UrlType_1780703823)
    - [ Mixins ](#cloc.mixins_1324909550)
        - [ cloc.mixins.Echo ](#cloc.mixins.Echo_178880302)
        - [ cloc.mixins.List ](#cloc.mixins.List_1486997353)
        - [ cloc.mixins.Version ](#cloc.mixins.Version_1196404455)
    - [ Viewsets ](#cloc.viewsets_343292859)
        - [ cloc.viewsets.GrpViewset ](#cloc.viewsets.GrpViewset_226248766)
        - [ cloc.viewsets.ReadOnlyViewset ](#cloc.viewsets.ReadOnlyViewset_1582907420)
        - [ cloc.viewsets.ReqSessionViewset ](#cloc.viewsets.ReqSessionViewset_902305522)
    - [ Helper Function ](#helper_function)
        - [ cloc.utils.echo ](#utils_echo)
        - [ cloc.utils.trace ](#utils_trace)
        - [ cloc.utils.listattrs ](#utils_listattrs)
- [ Advanced Usage Examples ](#examples)
    - [ Viewset Example ](#viewset_example)
    
<br>

<a name="install"></a>
## Installation
 *Virtual Environment is recommended*
```bash
pip3 install cloc
```
<br>

<a name="docs"></a>
## Documentation

<a name="cmd_and_grp"></a>
### Cmd and Grp

The two core features (classes) of CLOC, command line object chaining, are `Cmd` and `Grp`. 

A `Cmd` class object defines one action to process when invoked. In most cases, this will be the defined function that 
is decorated. A command can be invoked by calling the `Cmd` or being called by a `Grp`.

A `Grp` class object holds one to many actions to process when invoked. The actions can be a `Cmd` or another `Grp`, but
only one action can be called at a time per `Grp`. The first `Grp` will receive the first command 
line state, `sys.argv[1:]`. Every `Grp` will receive a command line state and will pass this state to the 
next action. It is on `Grp` only to update the command line state.

```python
from cloc import cmd, grp

@grp('cli')
def cli():
    """cli group"""
    pass

@cmd('hello-world')
def hello_world():
    """hello world function"""
    print('Hello World')

cli.add_command(hello_world)
cli()
```
`Grp` help structure. Usage will always be `grp` `name (cmd|grp)`
```bash
Cli

        cli group

USAGE: CLI NAME

Commands:
| Name                     | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| hello-world              | hello world function                                 |

```

---

<a name="parameters"></a>
### Parameters - Arg, Opt, and Flg

Currently parameters can only be given to a `Cmd`. 

The three core parameters include:
* `Arg` - a named positional argument for the command

        Arg(name: str, type: Any = str, help: str = None)
    
* `Opt` - a named non-positional argument for the command

        Opt(name: str, short_name: str, type: Any = str, default: Any= None, multiple: bool= False, 
            required: bool= False, help: str = None)

* `Flg` - a special version of `Opt` that is always type bool and expects no value
        
        Flg(name: str, short_name: str, help: str = None)

<br>
Below is an extended greeting cmd from above without the grp.

```python
from cloc import arg, cmd, flg, opt
from cloc.types import IntRange

@cmd('hello')
@arg('NAME', type=str, help='The person to greet')
@opt('--count', '-c', type=IntRange, default=1, help='Number of greetings: ex -c 0,5 OR -c 5')
@flg('--no_repeat', '-nr', help='If given, the greeting will not repeat')
def hello(name: str, count: IntRange, no_repeat: bool):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in count:
        print(f'Hello {name!r}')
        if no_repeat:
            break

if __name__ == '__main__':
    hello()
```
The below output is an example of a print message for the greeting cmd.
```bash
Hello

        Simple program that greets NAME for a total of COUNT times.

USAGE: hello NAME --count|-c [value] --no_repeat|-nr 

Parameters:
| Name               | Short    | Type             | Help                                                   |
| ------------------ | -------- | ---------------- | ------------------------------------------------------ |
| NAME               |          | str              | The person to greet                                    |
| --count            | -c       | cloc.IntRange    | [default: 1] Number of greetings: ex -c 0,5 OR -c 5    |
| --no_repeat        | -nr      | bool             | [flag] If given, the greeting will not repeat          |
```

---
 
<a name="classes"></a>
### Classes

<a name="cloc_basecmd"></a>
#### cloc.core.BaseCmd(name: str, params: Params= None, hidden: bool= False)

A base class that represents a basic command with a name, Params (`cloc.core.Params`), and a hidden option.
This class is meant to be inherited by new typs of commands. This class alone cannot invoke any functionality.

<a name="cloc_basecmd_values"></a>
##### `BaseCmd.values`: `list`

The values attribute is the list of arguments to be unpacked into the invoked function from the cmd

<a name="cloc_basecmd_params"></a>
##### `BaseCmd.params`: `cloc.core.Params`

The params attribute is the list of parameter objects defined for the cmd

<a name="cloc_basecmd__parse"></a>
##### `BaseCmd._parse(cmdl: list)`

Protected method to parse the current command line state. This will create the help string, create the param regex strings,
and get params values for the invoked `BaseCmd`. This method is protected and should normally not be called.

<a name="cloc_basecmd_create_help"></a>
##### `BaseCmd.create_help()`

The create_help method with create a formatted and colored help string using any params found

<a name="cloc_basecmd__print_help"></a>
##### `BaseCmd._print_help()`

Protected method to print the help message. This method can be overloaded in certain cases but is meant to call the help
attribute which might not exists in certain states.

<a name="cloc_basecmd_create_regex_patterns"></a>
##### `BaseCmd.create_regex_patterns()`

A method to be overloaded by a new command. This should create your regex patterns based on the defined parameters.

<a name="cloc_basecmd_get_values"></a>
##### `BaseCmd.get_values(cmdl: list)`

A method to be overloaded by a new command. After the regex patterns have been created, then the param values can be
parsed from the command line state and stored to be unpacked into the invoked command function.

---

<a name="cloc_cmd"></a>
#### cloc.core.Cmd(name: str, fn: Callable, params: Params = None, hidden: bool = False)

Cmd inherits BaseCmd to create a new command that can invoke a given function and be connected to class objects.

<a name="cloc_cmd_fn"></a>
##### `Cmd.fn`: `Callable`

The fn attribute is the defined function to run when cmd is invoked

<a name="cloc_cmd_dataclass"></a>
##### `Cmd.dataclass`: `object`

The dataclass attribute is an object to replace `self` with if the cmd is defined inside a class

<a name="cloc_cmd_new_dataclass_cmd"></a>
##### `Cmd.new_dataclass_cmd(cls, name: str, fn: Callable, params: Params= None, hidden: bool= False, dataclass: object= None)`
`Classmethod`

This class method will create a new Cmd that will have the dataclass attribute set

<a name="cloc_cmd_create_regex_patterns"></a>
##### `Cmd.create_regex_patterns()`

Create regex patterns for each opt and flg param to match against the command line state during get_values

<a name="cloc_cmd_get_values"></a>
##### `Cmd.get_values(cmdl: list)`

Overloaded function from BaseCmd, this method will create the values to be unpacked into `Cmd.fn`.
If `--help` is anywhere the command line, the help message for the nearest Cmd is called.

---

<a name="cloc_grp"></a>
#### cloc.core.Grp(name: str, commands: List[Cmd] = None, hidden:bool= False)

Grp inherits from BaseCmd, this class holds a list of Cmd objects which can be invoked by name. If Grp calls
Grp, the command line state will be updated. If a Grp is made with no cmdl supplied then sys.argv[1:] is used.

<a name="cloc_grp_commands"></a>
##### `Grp.commands`: `List[Cmd]`

The commands attribute is a list of Cmd objects. Cmd objects are added through the `Grp.add_command` method.

<a name="cloc_grp_invoke"></a>
##### `BaseCmd.invoke`: `str`

The invoke attribute is user input from the command line and should match a `Cmd.name` in `Grp.commands`

<a name="cloc_grp_cmdl"></a>
##### `BaseCmd.cmdl`: `list`

The cmdl attribute should represent the current state of the command line for the Grp to parse.

<a name="cloc_grp_add_command"></a>
##### `BaseCmd.add_command(command: BaseCmd, hidden:bool= None)`

Add a Cmd or Grp to another Grp. Can also override or set hidden state

This method will also make a new dataclass Cmd if needed. If a command is found inside a class,
initiate a dataclass Cmd to be made. Setting `dataclass = class that declared the commands`.
* a dataclass Cmd is the magic to allow Cli Viewsets and Querysets

<a name="cloc_grp_get_command"></a>
##### `BaseCmd.get_command(name: str)`

Find a Cmd by name and return the object

---

<a name="decorators"></a>
### Decorators

As seen in the above examples, decorators can be used to easily convert defined functions into a cmd or grp.
There is a decorator for each core class in cloc. They are imported into the cloc module for ease of use.

<a name="decorators_cmd"></a>
##### `cloc.decorators.cmd(name:str = None, hidden:bool = False)`

Returns a new Cmd object

<a name="decorators_grp"></a>
##### `cloc.decorators.grp(name:str = None, hidden:bool = False)`

Returns a new Grp object

<a name="decorators_arg"></a>
##### `cloc.decorators.arg(name:str, type: Any= None, help: str= None)`

Returns a Cmd object. If the object being decorated is already a Cmd object, the Arg will be appended to Cmd.params

<a name="decorators_opt"></a>
##### `cloc.decorators.opt(name:str, short_name: str, type: Any= None, default: Any= None, multiple:bool= False, required: bool= False, help: str= None)`

Returns a Cmd object. If the object being decorated is already a Cmd object, the Opt will be appended to Cmd.params

<a name="decorators_flg"></a>
##### `cloc.decorators.flg(name:str, short_name: str, help: str= None)`

Returns a Cmd object. If the object being decorated is already a Cmd object, the Flg will be appended to Cmd.params

---

<a name="cloc.types_2119495137"></a>
## Types

New types can be made to be used to convert the command line input. A new cloc type must inherit the 
`cloc.types.BaseType` and overload the `__call__` function to convert the input. New types can raise an exception or 
print to trace for a clean exit.

<a name="cloc.types.BaseType_1669657826"></a>
### cloc.types.BaseType(self, basetype: Any = None)

BaseType - BaseType object for creating new Param types

       __call__ method should be overloaded to handle value; str -> BaseType
    

<a name="BaseType.__call___1591412620"></a>
#### `BaseType.__call__(self, value: str)`

convert to new type

        Args:
            value {str} -- value to convert
        

<a name="cloc.types.Choices_1347752155"></a>
### cloc.types.Choices(self, choices: list, basetype: Any = typing.Any)

Convert input into a Choices object which will verify the input is contained in the defined choices.


<a name="cloc.types.DateType_974986765"></a>
### cloc.types.DateType(self)

Convert input into a DateTime object


<a name="cloc.types.FileType_442405428"></a>
### cloc.types.FileType(self)

Convert input into a file object. The below example is the `cloc.types.FileType` implementation

```python
class FileType(BaseType):
    __name__ = 'cloc.File'

    def __init__(self):
        # init should provide a base type, default to str
        super().__init__(io.TextIOWrapper)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fobj.close()

    def __call__(self, filepath: str):
        if not os.path.exists(filepath):
            trace(f'Error: {filepath!r} does not  exists', TypeError)
        elif not os.path.isfile(filepath):
            trace(f'Error: {filepath!r} is not a file', TypeError)
        self.fobj = open(filepath, 'r')
        return self.fobj
```

<a name="FileType.__exit___1883566034"></a>
#### `FileType.__exit__(self, exc_type, exc_val, exc_tb)`

File object will be closed in the exit function for the FileType class

<a name="cloc.types.IntRangeType_483716711"></a>
### cloc.types.IntRangeType(self)

Convert input to an Int Range [0 ... 5]

<a name="cloc.types.JsonType_806135893"></a>
### cloc.types.JsonType(self)

Convert input to type dict

<a name="cloc.types.Sha256Type_897860609"></a>
### cloc.types.Sha256Type(self)

Convert input into valid sha256, or if file path is found as input all valid sha256 values in the file

<a name="cloc.types.UrlType_1780703823"></a>
### cloc.types.UrlType(self)

Convert input into a valid URL

---

<a name="cloc.mixins_1324909550"></a>
## Mixins

Cloc mixins are a simple way to inherit cli functionality to your class. Below is an example of a Version mixin.
This enables a class to inherit a 'version' cmd. It will then look for the class attribute version and print it to the
 user.

```python
class Version(object):
    """Version Mixin - class object for easily adding an version command to a class
        - echo the 'version' attribute if it exists
    """

    def __call__(self):
        return self.version_cmd

    @cmd('version')
    def version_cmd(self):
        """version mixin command"""
        echo(cls=self, attribute='version', color='blue')
```

The below mixins are currently offered by cloc.

<a name="cloc.mixins.Echo_178880302"></a>
### cloc.mixins.Echo(self, *args, **kwargs)

Echo Mixin - class object for easily adding an echo command to a class
        - echo value of attributes by name

<a name="cloc.mixins.List_1486997353"></a>
### cloc.mixins.List(self, *args, **kwargs)

List Mixin - class object for easily adding an list command to a class
        - list attributes and values of the tied class

<a name="cloc.mixins.Version_1196404455"></a>
### cloc.mixins.Version(self, *args, **kwargs)

Version Mixin - class object for easily adding an version command to a class
        - echo the 'version' attribute if it exists

---

<a name="cloc.viewsets_343292859"></a>
## Viewsets

Viewsets are classes of commands that can be inherited into other classes. For example if you have a class that you
want to be able to query information from but not write to, you could use a ReadOnlyViewset that only gives the user
the option the print and list attributes from the class.

A viewset can also be made into a Queryset if the `GrpViewset` is inherited and the queryset attribute is set.
This then enables a user to override methods to retrieve data for the cli interface. A queryset could connect to a
database to retrieve information for the user based on defined commands.

Viewsets and Querysets become very useful in large CLI applications.

<a name="cloc.viewsets.GrpViewset_226248766"></a>
### cloc.viewsets.GrpViewset(self, *args, **kwargs)

A base Viewset that does not have any commands by default. The GrpViewset contains the queryset attribute and can be 
set for overloading data retrieval.


<a name="cloc.viewsets.ReadOnlyViewset_1582907420"></a>
### cloc.viewsets.ReadOnlyViewset(self, *args, **kwargs)

Read only viewset
    echo (print attribute by name)
    list (print all attribute names and values)
    version(print the current version of the Viewset based on the version attribute)


<a name="cloc.viewsets.ReqSessionViewset_902305522"></a>
### cloc.viewsets.ReqSessionViewset(self, *args, session: requests.sessions.Session = None, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16, raise_exception: bool = True, **kwargs)

Requests Session Viewset
    get (a cli cmd for session.get)

---

<a name="helper_functions"></a>
### Helper Functions

<a name="utils_echo"></a>
##### `cloc.utils.echo(message: Union[str, tuple, list, dict]= None, cls: object= None, attribute: str= None, list_delimiter: str = '\n', show_type: bool = False, indent: int= 4, color: str= None)`

Formats and colors a message, or class attribute.
* Pretty print tuple, list, and dict objects
* Customize the list delimiter and indent level for pretty print
* Color output
* Print the type for the output

prints the formatted string

<a name="utils_trace"></a>
##### `cloc.utils.trace(message:str, exception: Exception= None, raise_exception: bool= False, exit_code: int= 0, color: str= None)`

Formats and colors the output of a simplified traceback message.
* Utilizes the echo util for formatted and colored output
* Can accept and raise any type of Exception with the message
* Give an exit code to return with if exception is not raised

prints the formatted string and calls `sys.exit(exit_code)` or raises the given Exception (Assert) used if none given

<a name="utils_listattrs"></a>
##### `cloc.utils.listattrs(cls: object, verbose:bool=False)`

List the attributes and values of a given class object. If verbose is True, python defined attributes 
will also be included.
* Utilizes the echo util for formatted output

<br>

<a name="examples"></a>
## Advanced Usage Examples

<a name="viewset_example"></a>
### Using a viewset
```python
from cloc import grp
from cloc.viewsets import ReqSessionViewset

@grp('cli')
def cli():
    """requests session cli"""
    pass

session_viewset = ReqSessionViewset(raise_exception=False)

cli.add_command(session_viewset)

if __name__ == '__main__':
    cli()
```
The get command is implemented by the ReqSessionViewset and does not have to be defined
```bash
$ python example3.py get https://jsonplaceholder.typicode.com/todos/1
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}

```
<br>