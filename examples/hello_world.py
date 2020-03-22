from cloc import cmd, grp, flg, arg


@grp('cli')
@flg('--debug', '-d', help='debug mode')
def cli(debug: bool):
    """cli group"""
    if debug:
        print('debug enabled')

@cmd('hello-world')
@arg('name', type=str, help='name to print helloworld')
def hello_world(name: str):
    """hello world function"""
    print(f'Hello, {name!r}')

cli.add_command(hello_world)
cli()