"""
This file includes a class to abstract read/write functions
to work with STDIN/OUT or a file.
This is to simplify unit testing CLI menu writes and
user command entry.
"""

import logging

from typing import Optional
from pathvalidate import sanitize_filename
import sys

log = logging.getLogger(__name__)

class AbstractInputOutput():
    """
    Main Class for read/write abstraction.
    """

    def __init__(self):
        """
        Read/write abstraction initialisation.
        """

        # Initialise default file output name and mode.
        self._out_file = None
        self._open_mode = "w"
        self._of_handle = None

        # Open default application out 'file'.
        self.open_out()

    def set_out(self, o_file: Optional[str]) -> None:
        """
        Set the output file
        None is used to specify stdout.

        Args:
            o_file: Output filename.
        """

        # Set output file as required.
        # Need to sanitise the filename.
        if o_file:
            self._out_file = sanitize_filename(o_file)
        else:
            self._out_file = None

        # Open the output file for writing.
        self.open_out()

    def set_mode(self, mode: Optional[str]) -> None:
        """
        Set the output write mode.
        Set to "t" if not specified correctly.

        Args:
            mode:   Output write mode.
        """

        # Set output open mode.
        # Only support 'w', 'a', and 'b' modes.
        # If not in a valid output mode set to 'w'.
        if mode in ["w","a", "b"]:
            self._open_mode = mode
        else:
            self._open_mode = "w"

        # Open the output file for writing.
        self.open_out()

    def open_out(self) -> None:
        """
        Open the output file.
        """

        # Check if a filename has be specified,
        # if not use stdout instead.
        if self._out_file:
            try:
                self._of_handle = open(self._out_file, self._open_mode)
            except Exception as e:
                print(f"bad file name - {e}")
        else:
            self._of_handle = sys.stdout

    def close_out(self) -> None:
        """
        Close the output file.
        """

        # Close file if open.
        if self._of_handle:
            self._of_handle.close()

    def app_out(self, msg: str) -> None:
        """
        Application write, to either file or stdout.

        Args:
            msg:    Message to write to output file.
        """

        print(msg, file=self._of_handle)
