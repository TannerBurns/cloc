from cloc import cmd, grp, flg, arg


@grp('cli')
@arg('name', type=str, help='name to print helloworld')
@flg('--debug', '-d', help='debug mode')
def cli(name: str, debug: bool):
    """cli group"""
    print(name)
    if debug:
        print('debug enabled')

@cmd('hello-world')
def hello_world():
    """hello world function"""
    print('Hello World')

cli.add_command(hello_world)
cli()