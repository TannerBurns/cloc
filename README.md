# Command Line Object Chaining - cloc

<!--Badges-->
![MIT badge](https://img.shields.io/badge/license-MIT-black)
![Python3.6 badge](https://img.shields.io/badge/python-v3.6+-blue?logo=python&logoColor=yellow)
![Platform badge](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win32-yellow)

    Modern cli framework for simple and complex cli applications

# ToC
- [ Requirements ](#requirements)
- [ Installation ](#install)
- [ Documentation ](#docs)
    - [ Cmd and Grp ](#cmd_and_grp)
    - [ Parameters - Arg, Opt, and Flg ](#parameters)
    - [ Classes ](#classes)
        - [ BaseCmd ](#cloc_basecmd)
            - [ BaseCmd._parse ](#cloc_basecmd__parse)
            - [ BaseCmd.create_help ](#cloc_basecmd_create_help)
            - [ BaseCmd._print_help ](#cloc_basecmd__print_help)
            - [ BaseCmd.create_params_regex ](#cloc_basecmd_create_params_regex)
            - [ BaseCmd.get_params_values ](#cloc_basecmd_get_params_values)
    - [ Decorators ](#decorators)
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
$ git clone https://www.github.com/tannerburns/cloc
$ cd cloc
$ pip3 install .
```
<br>

<a name="docs"></a>
## Documentation
    Command line framework for making simple and complex command line applications.
* Easily group commands together
* Connect commands with classes for querysets
* Create command line viewsets for abstracting user interaction on command querysets
<br>

---

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

A base class that represents a basic command object with a name, Params (`cloc.core.Params`), and a hidden option.
This class is meant to be inherited by new command classes. 
Refer to `Cmd` or `Grp` for an inherited `BaseCmd` example.

<a name="cloc_basecmd__parse"></a>
##### `BaseCmd._parse(cmdl: list)`

Protected method to parse the current command line state. This will create the help string, create the param regex strings,
and get params values for the invoked `BaseCmd`. This method is protected and should normally not be called.

<a name="cloc_basecmd_create_help"></a>
##### `BaseCmd.create_help()`

A method to be overloaded by a new command. This should create a help message to print in the case `--help` is found in
the command line state.

<a name="cloc_basecmd__print_help"></a>
##### `BaseCmd._print_help()`

Protected method to print the help message. This method can be overloaded in certain cases but is meant to call the help
attribute which might not exists in certain states.

<a name="cloc_basecmd_create_params_regex"></a>
##### `BaseCmd.create_params_regex()`

A method to be overloaded by a new command. This should create your regex patterns based on the defined parameters.

<a name="cloc_basecmd_get_params_values"></a>
##### `BaseCmd.get_params_values(cmdl: list)`

A method to be overloaded by a new command. After the regex patterns have been created, then the param values can be
parsed from the command line state and stored to be unpacked into the invoked command function.
 ---
 
<a name="decorators"></a>
### Decorators

As seen in the above examples, decorators can be used to easily convert defined functions into a cmd or grp.
There is a decorator for each core class in cloc. They are imported into the cloc module for ease of use.

Core:
* `cmd` - easily create a new Cmd

        cmd(name:str = None, hidden:bool = False)

* `grp` - easily create a new Grp

        grp(name:str = None, hidden:bool = False)

Parameters:
* `arg` - create a new Arg

        arg(name:str, type: Any= None, help: str= None)

* `opt` - create a new Opt

        opt(name:str, short_name: str, type: Any= None, default: Any= None, multiple:bool= False, 
            required: bool= False, help: str= None)

* `flg` - create a new Flg

        flg(name:str, short_name: str, help: str= None)
 

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

<a name="queryset_example"></a>
### Using a queryset
```python
from cloc import grp
from cloc.viewsets import ReadOnlyViewset, GrpQueryset

@grp('cli')
def cli():
    """user and permissions queryset cli"""
    pass

@grp('users1')
def users1():
    """users1 queryset"""
    pass

@grp('perms1')
def perms1():
    """perms1 queryset"""
    pass

@grp('users2')
def users2():
    """users2 queryset"""
    pass

@grp('perms2')
def perms2():
    """perms2 queryset"""
    pass

class UserViewset(ReadOnlyViewset):
    version = '1.0.0'
    queryset = GrpQueryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PermissionViewset(ReadOnlyViewset):
    version = '0.0.1'
    queryset = GrpQueryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


uvs1 = UserViewset(users=['user1', 'user2'])
pvs1 = PermissionViewset(roles=['role1', 'role2'])
uvs2 = UserViewset(users=['user1', 'user2', 'user3'])
pvs2 = PermissionViewset(roles=['role1', 'role2', 'role3'])

perms1.add_command(pvs1)
users1.add_command(uvs1)
users1.add_command(perms1)

perms2.add_command(pvs2)
users2.add_command(uvs2)
users2.add_command(perms2)

cli.add_command(users1)
cli.add_command(users2)

if __name__ == '__main__':
    cli()
```
```bash
$ python example2.py users1 list
'users' user1, user2
'version' 1.0.0

$ python example2.py users2 list
'users' user1, user2, user3
'version' 1.0.0

```
<br>


<!--


<a name="cloc_cmd"></a>
### cloc.core.Cmd(name: str, fn: Callable, params: Params= None, hidden: bool= False)

This is the core class for creating new commands that can invoke a defined function. 
-->