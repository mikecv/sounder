"""
This file includes the CLI menu driven interface for the application,
as well as functions called by the menu options.

Installation of sound analysis was done via the Poetry environment.
Still required to install pyAudio support at the platform level via:
sudo apt install python3-pyaudio
"""

import logging

from scipy.io.wavfile import write  # type: ignore
import sounddevice as sd  # type: ignore

from sounder import std_io as io

MENU_ITEMS = {
    1: "Record sample",
    2: "Save sample",
    3: "Load sample",
    4: "Play sample",
    5: "Analyse sample",
    6: "Exit",
}

log = logging.getLogger(__name__)


def application_menu(app_io:io.AbstractInputOutput) -> None:
    """
    Runs a command line menu driven interface for the life of the application.
    """

    log.info("Starting application command menu.")

    while True:
        # Print a menu title.
        title_string = "   Sound Analyser   "
        app_io.app_out("=" * len(title_string))
        app_io.app_out(title_string)
        app_io.app_out("=" * len(title_string))

        # Print the menu for user selection.
        for key, value in MENU_ITEMS.items():
            app_io.app_out(f" <{key}> - {value}")

        # Get the user selection.
        app_io.app_out("\nMenu Selection : ", False)
        option = app_io.app_in()
        option = option.strip()

        # Process user selection.
        if option == "1":
            record_sample()
        elif option == "2":
            app_io.app_out("2 selected.")
        elif option == "3":
            app_io.app_out("3 selected.")
        elif option == "4":
            app_io.app_out("4 selected.")
        elif option == "5":
            app_io.app_out("5 selected.")
        elif option == "6":
            break
        else:
            app_io.app_out("Invalid selection.")


def record_sample() -> None:
    """
    Function to allow user to record an audio sample.
    The audio sample will be saved to memory.
    The user will have the option to play the audio sample,
    or to save it to a file from the main menu.
    """

    log.info("User selection to record audio sample.")

    # Sampling frequency
    freq = 44100

    # Recording duration
    duration = 5

    # Start recorder with the given values of
    # duration and sample frequency.
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency.
    write("recording.wav", freq, recording)
