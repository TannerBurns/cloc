# Command Line Object Chaining - cloc

<!--Badges-->
![MIT badge](https://img.shields.io/badge/license-MIT-black)
![Python3.6 badge](https://img.shields.io/badge/python-v3.6+-blue?logo=python&logoColor=yellow)
![Platform badge](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win32-yellow)

    Modern cli framework for simple and complex cli applications

# ToC
- [ Requirements ](#requirements)
- [ Installation ](#install)
- [ Information ](#information)
- [ Examples ](#examples)
    - [ Simple Example ](#simple-example)
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

<a name="information"></a>
## Information
    Command line framework for making simple and complex command line applications.
* Easily group commands together
* Connect commands with classes for querysets
* Create command line viewsets for abstracting user interaction on command querysets
<br><br>

<a name="#examples"></a>
## Examples

<a name="#simple_example"></a>
### Simple example
```python
from cloc import cmd, grp, opt
from cloc.types import IntRange

@grp('cli')
def cli():
    """base cli"""
    pass

@cmd('hello')
@opt('--count', '-c', type=IntRange, default=1, help='Number of greetings: ex -c 0,5 OR -c 5')
@opt('--name', '-n', type=str, help='The person to greet')
def hello(count: IntRange, name: str):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in count:
        print(f'Hello {name!r}')

if __name__ == '__main__':
    cli.add_command(hello)
    cli()
```
```bash
$ python example4.py hello --help

Hello

        Simple program that greets NAME for a total of COUNT times.

USAGE: hello --count|-c [value] --name|-n [value] 

Parameters:
| Name               | Short    | Type             | Help                                                   |
| ------------------ | -------- | ---------------- | ------------------------------------------------------ |
| --count            | -c       | cloc.IntRange    | [default: 1] Number of greetings: ex -c 0,5 OR -c 5    |
| --name             | -n       | str              | [default: None] The person to greet                    |

```
<br>

<a name="#viewset_example"></a>
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

<a name="#queryset_example"></a>
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