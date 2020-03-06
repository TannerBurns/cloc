from cloc import cmd, grp,  flg

@grp('cli')
@flg('--debug', '-d', help='debug mode')
def cli(debug: bool):
    """cli group"""
    if debug:
        print('debug enabled')
    pass

@cmd('hello-world')
def hello_world():
    """hello world function"""
    print('Hello World')

cli.add_command(hello_world)
cli()