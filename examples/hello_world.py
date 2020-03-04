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