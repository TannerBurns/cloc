from cloc import cmd, grp, opt
from cloc.types import IntRange

@grp('cli')
def cli():
    """base cli"""
    pass

@cmd('hello')
@opt('--count', '-c', type=IntRange, default=1, help='Number of greetings: ex -c 0,5 OR -c 5')
@opt('--name', '-n', type=str, help='The person to greet')
def hello(count: IntRange, name: str):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in count:
        print(f'Hello {name!r}')

if __name__ == '__main__':
    cli.add_command(hello)
    cli()
