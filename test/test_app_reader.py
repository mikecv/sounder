"""
Unit test for application menu reader.
Using redirection from stdin to file.
"""

from sounder import std_io as io

def test_input_from_file():

    # Instatiate the app IO class.
    aw = io.AbstractInputOutput()

    # Create a test file with some input commands.
    test_file = "test_file.tst"
    with open (test_file, "w", encoding="utf8") as outfile:
        outfile.write("1\n")
        outfile.write("2\n")
        outfile.write("3\n")
    outfile.close()

    # Open the file for reading.
    aw.set_in_file("test_file.tst")

    # Simulate the input commands.
    line = aw.app_in().splitlines()
    assert line[0] == "1"
    line = aw.app_in().splitlines()
    assert line[0] == "2"
    line = aw.app_in().splitlines()
    assert line[0] == "3"
    print(line[0])

    # Close the input file.
    aw.close_in
    