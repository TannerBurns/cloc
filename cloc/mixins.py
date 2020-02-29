
from cloc import arg, cmd
from cloc.utils import echoattr, listattrs

class Echo(object):

    def __call__(self):
        return self.echo

    @cmd('echo')
    @arg('attribute', type=str, help='attribute value to echo')
    def echo(self, attribute: str):
        """echo mixin command"""
        echoattr(self, attribute)

class List(object):

    def __call__(self):
        return self.list

    @cmd('list')
    def list(self):
        """list mixin command"""
        listattrs(self)
