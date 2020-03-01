
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