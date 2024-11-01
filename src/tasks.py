from pathlib import Path

from invoke import task, Context

here = Path(__file__).parent


@task(name='mautogen')
def autogen_migration(c: Context, m: str, ini: Path = Path('../alembic.ini')):
    """
                            -m: комментарий к миграции\n
    [--ini = '../alembic.ini']: путь до ini файла alembic
    """
    # print(f'alembic -c {here / ini} revision --autogenerate -m "{m}"')
    c.run(f'alembic -c {here / ini} revision --autogenerate -m "{m}"')


@task(name='mupgrade')
def do_migration(c: Context, revision: str = 'head', ini: Path = Path('../alembic.ini')):
    """
    [-r, --revision = 'head']: конкретная миграция\n
    [--ini = '../alembic.ini']: путь до ini файла alembic
    """
    c.run(f'alembic -c {here / ini} upgrade {revision}')
