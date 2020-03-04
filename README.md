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

- [ Requirements ](#requirements)
- [ Installation ](#install)
- [ Documentation ](#docs)
    - [ Cmd and Grp ](#cmd_and_grp)
    - [ Parameters - Arg, Opt, and Flg ](#parameters)
    - [ Classes ](#classes)
        - [ BaseCmd ](#cloc_basecmd)
            - [ BaseCmd.values ](#cloc_basecmd_values)
            - [ BaseCmd.params ](#cloc_basecmd_params)
            - [ BaseCmd._parse ](#cloc_basecmd__parse)
            - [ BaseCmd.create_help ](#cloc_basecmd_create_help)
            - [ BaseCmd._print_help ](#cloc_basecmd__print_help)
            - [ BaseCmd.create_regex_patterns ](#cloc_basecmd_create_regex_patterns)
            - [ BaseCmd.get_values ](#cloc_basecmd_get_values)
        - [ Cmd ](#cloc_cmd)
            - [ Cmd.fn ](#cloc_cmd_fn)
            - [ Cmd.dataclass ](#cloc_cmd_dataclass)
        - [ Grp ](#cloc_grp)
    - [ Decorators ](#decorators)
        - [ cloc.decorators.cmd ](#decorators_cmd)
        - [ cloc.decorators.grp ](#decorators_grp)
        - [ cloc.decorators.arg ](#decorators_arg)
        - [ cloc.decorators.opt ](#decorators_opt)
        - [ cloc.decorators.flg ](#decorators_flg)
    - [ Helper Function ](#helper_function)
        - [ cloc.utils.echo ](#utils_echo)
        - [ cloc.utils.trace ](#utils_trace)
        - [ cloc.utils.listattrs ](#utils_listattrs)
        - [ cloc.utils.defaultattr ](#utils_defaultattr)
- [ Advanced Usage Examples ](#examples)
    - [ Viewset Example ](#viewset-example)
    - [ Queryset Example ](#queryset-example)
<br><br>

<a name="requirements"></a>
## Requirements
* System
    * Python 3.6+
    
* Python Pip
    * requests
<br><br>

<a name="install"></a>
## Installation
 *Virtual Environment is recommended*
```bash
git clone https://www.github.com/tannerburns/cloc
cd cloc
pip3 install .
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

**TODO: Grp function should also get invoked and have parameters of its own**


Until the above is in place. The current behavior does not allow options on subcommands but only the active command.

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

---

<a name="cloc_grp"></a>
#### cloc.core.Grp(name: str, commands: List[Cmd] = None, hidden:bool= False)

Grp inherits BaseCmd to create a new type of command that holds one to many commands and can be chained together

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

<a name="utils_defaultattr"></a>
##### `cloc.utils.defaultattr(cls: object, attribute: str, default: Any= None)`

Return the value of the attribute if exists or set the default and return the attribute value

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