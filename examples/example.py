from cloc import grp, cmd, opt, arg, mixins

"""Test  Code ->"""

@grp('cli')
def cli():
    """cli"""
    pass

@grp('nested')
def group2():
    """group 2"""
    pass

@grp('permissions')
def permission_group():
    pass

@cmd('test')
@arg('arg1', type=int, help='positional argument 1')
@opt('--opt1', '-o1', type=str, help='option 1')
def test(cmd1, opt1=None):
    """test command"""
    print('#test_command')
    print(type(cmd1), type(opt1))
    print(cmd1, str(opt1))

class UserCmds(mixins.List, mixins.Echo):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @cmd('users')
    def listusers(self):
        """list users command"""
        print('#user_command')
        if hasattr(self, 'users'):
            print(', '.join(self.users))


class PermissionCmds(mixins.List, mixins.Echo):

    """this class is going to inherit the List mixin which provides a generic list command"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


u = UserCmds(users=['user1', 'user2'])
user2 = UserCmds(users=['user1', 'user2', 'user3'])
perms = PermissionCmds(roles=['admin', 'user', 'dev'], services=['test_service1'])

cli.add_command(u)
cli.add_command(group2)

group2.add_command(test)
group2.add_command(user2)
group2.add_command(permission_group)

permission_group.add_command(perms)


if __name__ == '__main__':
    cli()