"""
Command line progress bar class.
"""

import logging

import dotsi  # type: ignore

log = logging.getLogger(__name__)


class CLI_PROGRESS:

    """
    CLI Progress Bar Class.
    """

    def __init__(self, settings: dotsi.Dict, action: str):
        """
        CLI progress bar initialisation.
        Args:
            settings:   Application settings.
            action:     Action in progress (string)
        """

        log.info("Initialising CLI progress bar.")

        # Initialise progress bar settings to use.
        self._settings = settings
        self._action = action

    def show_progress(self, prog: int):

        # Calculate length of progress done and to do.
        left = self._settings.progress.BAR_WIDTH * prog // 100
        right = self._settings.progress.BAR_WIDTH - left

        # Complile strings to show progress.
        tags = "#" * left
        spaces = " " * right
        percents = f"{prog:.0f}%"

        # Print the progress bar.
        # Note printing on same line so first action
        # is to return to start of line.
        # Also, don't do new line at the end.
        print(f"\r{self._action} [{tags}{spaces}] {percents}", sep="", end="", flush=True)
