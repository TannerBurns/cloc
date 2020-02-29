
from cloc import arg, cmd, flg
from cloc.utils import echoattr, listattrs

class Echo(object):

    def __call__(self):
        return self.echo

    @cmd('echo')
    @arg('attribute', type=str, help='attribute value to echo')
    def echo_cmd(self, attribute: str):
        """echo mixin command"""
        echoattr(self, attribute)

class List(object):

    def __call__(self):
        return self.list

    @cmd('list')
    @flg('--verbose', '-v', help='Print all attributes')
    def list_cmd(self, verbose:bool=False):
        """list mixin command"""
        listattrs(self, verbose=verbose)

class Version(object):

    def __call__(self):
        return self.version

    @cmd('version')
    def version_cmd(self):
        """version mixin command"""
        echoattr(self, 'version')