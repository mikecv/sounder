"""
Unit test for application start-up.
"""

import logging

from datetime import datetime
from sounder import std_io as io

log = logging.getLogger(__name__)


def test_output_to_file():

    # Instatiate the app IO class.
    aw = io.AbstractInputOutput()

    # Set output to a testfile
    test_out_file = "test-file.txt"
    aw.set_out(test_out_file)
    # Contents to test with.
    test_stuff = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
    # Write to the file
    aw.app_out(test_stuff)
    aw.close_out()

    # Open the file and check that contents is as expected.
    # Strip the newline from the read file before comparison.
    fh = open(test_out_file, "r")
    contents = fh.read().splitlines()
    fh.close()
    assert contents[0] == test_stuff

def test_output_to_file_append():

    # Instatiate the app IO class.
    aw = io.AbstractInputOutput()

    # Set output to a testfile
    test_out_file = "test-file.txt"
    aw.set_out(test_out_file)
    # Contents to test with.
    test_stuff = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
    # Write to the file
    aw.app_out(test_stuff)

    # Set to append mode and append more to the file.
    aw.set_mode("a")
    # Contents to test with.
    test_stuff_2 = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
    # Write (append) to the file
    aw.app_out(test_stuff_2)
    aw.close_out()

    # Open the file and check that contents is as expected.
    # Strip the newline from the read file before comparison.
    fh = open(test_out_file, "r")
    contents = fh.read().splitlines()
    fh.close()
    assert contents[0] == test_stuff
    assert contents[1] == test_stuff_2
