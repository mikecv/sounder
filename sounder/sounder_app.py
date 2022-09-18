"""
Sound analyser program.
"""

import logging

from sounder.app_logging import setup_logging

APP_NAME: str = "sounder"
APP_VERSION: str = "0.0.1"

log = logging.getLogger(APP_NAME)

class SoundAnalyser:
    """
    Main Class the sound analyser application.
    """

    def __init__(self):

        # Setup the application logger.
        setup_logging(APP_NAME)

        log.info(f"Starting application : {APP_NAME}, version : {APP_VERSION}")

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
