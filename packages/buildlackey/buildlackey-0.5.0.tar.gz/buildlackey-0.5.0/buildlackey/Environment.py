from logging import Logger
from logging import getLogger


class Environment:
    ENV_PROJECTS_BASE: str = 'PROJECTS_BASE'
    ENV_PROJECT:       str = 'PROJECT'

    def __init__(self):
        self.logger: Logger = getLogger(__name__)
