"""
Sound analyser program.
"""

import logging
import sys

import dotsi  # type: ignore

from sounder import app_settings
from sounder import menu_functions as menu
from sounder import std_io as io
from sounder.app_logging import setup_logging

log = logging.getLogger(__name__)


class SoundAnalyser:
    """
    Main Class the sound analyser application.
    """

    def __init__(self):
        """
        Sound analyser initialisation.
        """

        # Load application settings.
        self._settings = dotsi.Dict(app_settings.load("./sounder/settings.yaml"))

        # Initialise app name and version from settings.
        self._app_name = self._settings.app.APP_NAME
        self._app_version = self._settings.app.APP_VERSION

        # Setup the application logger.
        setup_logging(self._app_name)

        log.info(f"Starting application: {self._app_name}, version: {self._app_version}")

        # Instantiate application IO class.
        # Call with default arguements, i.e. IO from stdin and stdout.
        app_io = io.AbstractInputOutput(None, None, None)

        # Instantiate the menu class.
        # This drives the actions during the life of the application.
        # And set it running.
        main_menu = menu.AppMenu(self._settings, app_io)
        main_menu.run()


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
