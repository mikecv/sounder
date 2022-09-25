"""
This file includes the CLI menu driven interface for the application,
as well as functions called by the menu options.
"""

import logging

MENU_ITEMS = {
    1: "Record sample",
    2: "Load sample",
    3: "Save sample",
    4: "Play sample",
    5: "Analyse sample",
    6: "Exit",
}

log = logging.getLogger(__name__)


def application_menu() -> None:
    """
    Runs a command line menu driven interface for the life of the application.
    """

    log.info("Starting application command menu.")

    while True:
        # Print a menu title.
        title_string = "   Sound Analyser   "
        print("=" * len(title_string))
        print(title_string)
        print("=" * len(title_string))

        # Print the menu for user selection.
        for key, value in MENU_ITEMS.items():
            print(f" <{key}> - {value}")

        # Get the user selection.
        option = input(" \nSelection: ")
        option = option.strip()

        # Process user selection.
        if option == "1":
            record_sample()
        elif option == "2":
            print("2 selected.")
        elif option == "3":
            print("3 selected.")
        elif option == "4":
            print("4 selected.")
        elif option == "5":
            print("5 selected.")
        elif option == "6":
            break
        else:
            print("Invalid selection.")


def record_sample() -> None:
    """
    Function to allow user to record an audio sample.
    The audio sample will be saved to memory.
    The user will have the option to play the audio sample,
    or to save it to a file from the main menu.
    """

    log.info("User selection to record audio sample.")
