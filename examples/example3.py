
from cloc import grp
from cloc.viewsets import ReqSessionViewset

@grp('cli')
def cli():
    """cli"""
    pass

session_viewset = ReqSessionViewset(raise_exception=False)
@grp('session')
def session():
    """requests session"""
    pass

session.add_command(session_viewset)
cli.add_command(session)

if __name__ == '__main__':
    cli()