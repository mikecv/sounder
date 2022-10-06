"""
This file includes a class to abstract read/write functions
to work with STDIN/OUT or a file.
This is to simplify unit testing CLI menu writes and
user command entry.
"""

import logging
import sys
from typing import Optional

from pathvalidate import sanitize_filename

log = logging.getLogger(__name__)


class AbstractInputOutput:
    """
    Main Class for read/write abstraction.
    """

    def __init__(self, ifile: Optional[str], ofile: Optional[str], ofmode: Optional[str]) -> None:
        """
        Read/write abstraction initialisation.

        Args:
            ifile:  Input file name, stdin if None or not present.
            ofile:  Output file name, stdout if None or not present.
            ofmode: Output file open mode.
        """

        log.info("Initialising application IO.")

        # Initialise default file input name and mode.
        self._in_file = None
        self._if_open_mode = "r"
        self._if_handle = None

        # Initialise default file output name and mode.
        self._out_file = None
        self._of_open_mode = "w"
        self._of_handle = None

        # Update class arguements if given.
        self.set_in_file(ifile)
        self.set_out_file(ofile)
        self.set_out_mode(ofmode)

        # Open default application in 'file'.
        self.open_in()

        # Open default application out 'file'.
        self.open_out()

    def set_in_file(self, i_file: Optional[str]) -> None:
        """
        Set the input file.
        None is used to specify stdin.

        Args:
            i_file: Input filename, stdin if None or not present.
        """

        # Set input file as required.
        # Need to sanitise the filename.
        if i_file:
            self._in_file = sanitize_filename(i_file)
        else:
            self._in_file = None

        # Open the input file for reading.
        self.open_in()

    def open_in(self) -> None:
        """
        Open the input file.
        """

        # Check if a filename has been specified,
        # if not use stdin instead.
        if self._in_file:
            try:
                self._if_handle = open(self._in_file, self._if_open_mode, encoding="utf8")
            except FileNotFoundError as e:
                log.error(f"File not found - {e}")
        else:
            self._if_handle = sys.stdin

    def close_in(self) -> None:
        """
        Close the input file.
        """

        # Close file if open.
        if self._if_handle:
            self._if_handle.close()

    def app_in(self) -> str:
        """
        Application read, from either file or stdin.
        Reads one line at a time.

        Returns:
            String read from the file.
        """

        return self._if_handle.readline()

    def set_out_file(self, o_file: Optional[str]) -> None:
        """
        Set the output file.
        None is used to specify stdout.

        Args:
            o_file: Output filename, stdout if None or not present.
        """

        # Set output file as required.
        # Need to sanitise the filename.
        if o_file:
            self._out_file = sanitize_filename(o_file)
        else:
            self._out_file = None

        # Open the output file for writing.
        self.open_out()

    def set_out_mode(self, mode: Optional[str]) -> None:
        """
        Set the output write mode.
        Set to "w" if not specified correctly.

        Args:
            mode:   Output write mode, write mode if None or not present.
        """

        # Set output open mode.
        # Only support 'w', 'a', and 'b' modes.
        # If not in a valid output mode set to 'w'.
        if mode in ["w", "a"]:
            self._of_open_mode = mode
        else:
            self._of_open_mode = "w"

        # Open the output file for writing.
        self.open_out()

    def open_out(self) -> None:
        """
        Open the output file.
        """

        # Check if a filename has been specified,
        # if not use stdout instead.
        if self._out_file:
            try:
                self._of_handle = open(self._out_file, self._of_open_mode, encoding="utf8")
            except FileNotFoundError as e:
                log.error(f"File not found - {e}")
        else:
            self._of_handle = sys.stdout

    def close_out(self) -> None:
        """
        Close the output file.
        """

        # Close file if open.
        if self._of_handle:
            self._of_handle.close()

    def app_out(self, msg: str, nline: Optional[bool]=True) -> None:
        """
        Application write, to either file or stdout.

        Args:
            msg:    Message to write to output file.
            nline:  True to add a newline, false not to.
        """

        if nline:
            print(msg, file=self._of_handle)
        else:
            print(msg, file=self._of_handle, end="")
