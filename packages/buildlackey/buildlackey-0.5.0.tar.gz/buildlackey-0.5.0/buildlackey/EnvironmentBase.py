
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment

from buildlackey.Environment import Environment

from buildlackey.exceptions.ProjectNotSetException import ProjectNotSetException
from buildlackey.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException


class EnvironmentBase:
    """

    """
    def __init__(self):

        self.ebLogger: Logger = getLogger(__name__)

        self._projectsBase:     str = ''
        self._projectDirectory: str = ''

        try:
            self._projectsBase = osEnvironment[Environment.ENV_PROJECTS_BASE]
        except KeyError:
            self.ebLogger.error(f'Project Base not set')
            raise ProjectsBaseNotSetException
        try:
            self._projectDirectory = osEnvironment[Environment.ENV_PROJECT]
        except KeyError:
            self.ebLogger.error(f'Project Directory not set')
            raise ProjectNotSetException
        except (ValueError, Exception) as e:
            self.ebLogger.error(f'{e}')
