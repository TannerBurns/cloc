import sys
from cloc import grp, cmd, opt, arg
from cloc.utils import echoattr, listattrs

"""Test  Code ->"""

@grp('cli')
def cli():
    """cli"""
    pass

@grp('g2')
def group2():
    """group 2"""
    pass

@cmd('test')
@arg('arg1', type=str, help='positional argument 1')
@opt('--opt1', '-o1', type=str, help='option 1')
def test(cmd1, opt1=None):
    """test command"""
    print('#test_command')
    print(cmd1, str(opt1))

class UserCmds(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @cmd('users')
    def listusers(self):
        """list users command"""
        print('#user_command')
        if hasattr(self, 'users'):
            print(', '.join(self.users))


    @cmd('echo')
    @arg('attribute', type=str, help='attribute value to echo')
    def echo(self, attribute:str):
        """echo command"""
        print('#echo_command')
        echoattr(self, attribute)

    @cmd('list')
    def list(self):
        """list command"""
        print('#list_command')
        listattrs(self)


u = UserCmds(users=['user1', 'user2'])
user2 = UserCmds(users=['user1', 'user2', 'user3'])

cli.add_command(u)
cli.add_command(group2)

group2.add_command(test)
group2.add_command(user2)


if __name__ == '__main__':
    cli()