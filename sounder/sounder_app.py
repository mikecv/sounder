"""
Sound analyser program.
"""

import logging
import sys

from sounder import menu_functions as menu
from sounder.app_logging import setup_logging

APP_NAME: str = "sounder"
APP_VERSION: str = "0.0.1"

log = logging.getLogger(__name__)


class SoundAnalyser:
    """
    Main Class the sound analyser application.
    """

    def __init__(self):
        """
        Sound analyser initialisation.
        """

        self._app_name = APP_NAME
        self._app_version = APP_VERSION

        # Setup the application logger.
        setup_logging(self._app_name)

        log.info(f"Starting application : {self._app_name}, version : {self._app_version}")

        # Call commandline menu function.
        # This drives the actions during the life of the application.
        menu.application_menu()


def run() -> None:
    """
    Poetry calls this to get the application up and running.
    Assumes a python script as follows:

    [tool.poetry.scripts]
    sounder-go = "sounder.sounder_app:run"
    """

    SoundAnalyser()


if __name__ == "__main__":
    run()
