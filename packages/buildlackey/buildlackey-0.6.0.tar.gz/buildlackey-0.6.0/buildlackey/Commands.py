
from os import chdir

from os import sep as osSep
from os import system as osSystem

from click import argument
from click import clear
from click import command
from click import secho
from click import version_option

from buildlackey.Environment import EnvironmentBase
from buildlackey.Version import Version


# noinspection SpellCheckingInspection
UNIT_TEST_CLI: str = 'python3 -Wdefault -m tests.TestAll'

DELETE_DIST_BUILD:       str = 'rm -rfv dist build'
DELETE_GENERAL_EGG_INFO: str = "find . -type d -name '*'.egg-info -delete"
DELETE_LOG_FILES:        str = 'find . -type f -name "*.log"      -delete'
DELETE_EGGS:             str = 'rm -rfv .eggs'

PROJECTS_BASE: str = 'PROJECTS_BASE'
PROJECT:       str = 'PROJECT'


def changeToProjectRoot(projectsBase: str, project: str):

    fullPath: str = f'{projectsBase}{osSep}{project}'
    chdir(fullPath)


def doCommandStart(projects_base: str, project: str):
    clear()
    secho(f'{projects_base=}', color=True, reverse=True)
    secho(f'{project=}', color=True, reverse=True)
    secho('')
    changeToProjectRoot(projectsBase=projects_base, project=project)


@command()
@version_option(version=f'{Version().version}', message='%(prog)s version %(version)s')
def runtests():
    """
    \b
    Runs the unit tests for the project specified by the following environment variables;

    \b
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    \b
    However, if one or the other is not defined the command assumes it is executing in a CI
    environment and thus the current working directory is the project base directory.
    """
    envBase: EnvironmentBase = EnvironmentBase()
    if envBase.validProjectsBase is True and envBase.validProjectDirectory() is True:
        changeToProjectRoot(projectsBase=envBase.projectsBase, project=envBase.projectDirectory)

    secho(f'{UNIT_TEST_CLI}')
    status: int = osSystem(f'{UNIT_TEST_CLI}')
    secho(f'{status=}')


@command()
@version_option(version=f'{Version().version}', message='%(prog)s version %(version)s')
@argument('projects_base', envvar=PROJECTS_BASE)
@argument('project',       envvar=PROJECT)
def cleanup(projects_base: str, project: str):
    """
    \b
    Clean the build artifacts for the project specified by the following environment variables
    \b
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """
    doCommandStart(projects_base, project)

    secho(f'{DELETE_DIST_BUILD}')
    status: int = osSystem(DELETE_DIST_BUILD)
    secho(f'{status=}')

    secho(f'{DELETE_GENERAL_EGG_INFO}')
    status = osSystem(DELETE_GENERAL_EGG_INFO)
    secho(f'{status=}')

    secho(f'{DELETE_LOG_FILES}')
    status = osSystem(DELETE_LOG_FILES)
    secho(f'{status=}')

    secho(f'{DELETE_EGGS}')
    status = osSystem(DELETE_EGGS)
    secho(f'{status=}')

    PROJECT_EGG_INFO: str = f'rm -rfv {project}.egg-info'
    secho(f'{PROJECT_EGG_INFO}')
    status = osSystem(PROJECT_EGG_INFO)
    secho(f'{status=}')


@command()
@version_option(version=f'{Version().version}', message='%(prog)s version %(version)s')
@argument('projects_base', envvar=PROJECTS_BASE)
@argument('project',       envvar=PROJECT)
def runmypy(projects_base: str, project: str):
    """
    \b
    Runs the mypy checks for the project specified by the following environment variables
    \b
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """
    doCommandStart(projects_base, project)

    # noinspection SpellCheckingInspection
    # noinspection SpellCheckingInspection
    RUN_MYPY: str = f'mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --check-untyped-defs  {project} tests'
    secho(f'{RUN_MYPY}')

    status: int = osSystem(RUN_MYPY)
    secho(f'{status=}')


@command()
@version_option(version=f'{Version().version}', message='%(prog)s version %(version)s')
@argument('projects_base', envvar=PROJECTS_BASE)
@argument('project',       envvar=PROJECT)
def deploy(projects_base: str, project: str):
    """
    \b
    Creates the deployable for the project specified by the following environment variables
    \b
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """
    doCommandStart(projects_base, project)

    BUILD_WHEEL:   str = 'python -m build --sdist --wheel'
    secho(f'{BUILD_WHEEL}')
    status: int = osSystem(BUILD_WHEEL)
    secho(f'{status=}')

    CHECK_PACKAGE: str = 'twine check dist/*'
    secho(f'{CHECK_PACKAGE}')
    status = osSystem(CHECK_PACKAGE)
    secho(f'{status=}')


@command()
@version_option(version=f'{Version().version}', message='%(prog)s version %(version)s')
@argument('projects_base', envvar=PROJECTS_BASE)
@argument('project', envvar=PROJECT)
def prodpush(projects_base: str, project: str):
    """
    \b
    Pushes the deployable to pypi.  The project is specified by the following environment variables
    \b
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """
    doCommandStart(projects_base, project)

    PYPI_PUSH: str = 'twine upload  dist/*'

    secho(f'{PYPI_PUSH}')
    status = osSystem(PYPI_PUSH)
    secho(f'{status=}')


if __name__ == "__main__":

    runtests()
