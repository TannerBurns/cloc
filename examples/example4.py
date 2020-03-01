
from cloc import cmd, grp, opt

@grp('cli')
def cli():
    """base cli"""
    pass

@cmd('hello')
@opt('--count', '-c', type=int, default=1, help='Number of greetings')
@opt('--name', '-n', type=str, help='The person to greet')
def hello(count: int, name: str):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in  range(count):
        print(f'Hello {name!r}')

if __name__ == '__main__':
    cli.add_command(hello)
    cli()
