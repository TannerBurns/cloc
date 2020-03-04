from cloc import arg, cmd, flg, opt
from cloc.types import IntRange

@cmd('hello')
@arg('NAME', type=str, help='The person to greet')
@opt('--count', '-c', type=IntRange, default=1, help='Number of greetings: ex -c 0,5 OR -c 5')
@flg('--no_repeat', '-nr', help='If given, the greeting will not repeat')
def hello(name: str, count: IntRange, no_repeat: bool):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in count:
        print(f'Hello {name!r}')
        if no_repeat:
            break

if __name__ == '__main__':
    hello()