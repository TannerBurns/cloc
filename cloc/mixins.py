from cloc import arg, cmd, flg
from cloc.utils import echo, listattrs

class Echo(object):
    """Echo Mixin - class object for easily adding an echo command to a class
        - echo value of attributes by name
    """

    def __call__(self):
        return self.echo_cmd

    @cmd('echo')
    @arg('attribute', type=str, help='attribute value to echo')
    def echo_cmd(self, attribute: str):
        """echo mixin command"""
        echo(cls=self, attribute=attribute)

class List(object):
    """List Mixin - class object for easily adding an list command to a class
        - list attributes and values of the tied class
    """

    def __call__(self):
        return self.list_cmd

    @cmd('list')
    @flg('--verbose', '-v', help='Print all attributes')
    def list_cmd(self, verbose:bool=False):
        """list mixin command"""
        listattrs(self, verbose=verbose)

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