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
        left = self._settings.progress.PROG_WIDTH * prog // 100
        right = self._settings.progress.PROG_WIDTH - left
        # Determine progress bar through warning point.
        if left < self._settings.progress.BAR_WARNING:
            left_normal = left
            left_warning = 0
            right_normal = self._settings.progress.BAR_WARNING - left
            right_warning = right - right_normal
        else:
            left_normal = self._settings.progress.BAR_WARNING
            left_warning = left - left_normal
            right_normal = 0
            right_warning = right

        # Complile strings to show progress.
        # Show progress and remainder taking account of warning level.
        prog_n = "#" * left_normal
        prog_w = "#" * left_warning
        rem_n = "-" * right_normal
        rem_w = "-" * right_warning
        percents = f"{prog:.0f}%"

        # Print the progress bar.
        # Note printing on same line so first action
        # is to return to start of line.
        # Also, don't do new line at the end.
        # Show progress and remaining in different colours.
        print(
            f"\r{self._action} [\033[1;32m{prog_n}\033[1;31m{prog_w}\033[0;32m{rem_n}\033[0;31m{rem_w}\033[0m] {percents}",
            sep="",
            end="",
            flush=True,
        )
