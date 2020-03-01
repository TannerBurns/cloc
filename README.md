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
```python
from cloc import cmd, grp, opt

@grp('cli')
def cli():
    """base cli"""
    pass

@cmd('hello')
@opt('--count', '-c', type=int, default=1, help='Number of greetings')
@opt('--name', '-n', type=str, help='The person to greet')
def hello(count: int, name: str):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in  range(count):
        print(f'Hello {name!r}')

if __name__ == '__main__':
    cli.add_command(hello)
    cli()
```
    