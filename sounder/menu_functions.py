"""
This file includes the CLI menu driven interface for the application,
as well as functions called by the menu options.

Installation of sound analysis was done via the Poetry environment.
Still required to install pyAudio support at the platform level via:
sudo apt install python3-pyaudio
"""

from datetime import datetime
import logging
from typing import Optional

import dotsi  # type: ignore
from scipy.io.wavfile import write  # type: ignore
import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore

from sounder import std_io as io
import sounder.sound_plot as splot

MENU_ITEMS = {
    1: "Record sample",
    2: "Load sample",
    3: "Play sample",
    4: "Analyse sample",
    5: "Exit",
}

log = logging.getLogger(__name__)


class AppMenu:
    """
    Main Class for application.
    """

    def __init__(self, settings: dotsi.Dict, app_io: io.AbstractInputOutput) -> None:
        """
        Main menu initialisation.
        Args:
            settings:   Application settings.
            app_io:     Input / Output class object to use.
        """

        log.info("Initialising main menu.")

        # Initialise application settings to use.
        self._settings = settings

        # Initialise app io abstraction to use.
        self.app_io = app_io

        # Initialise stay alive.
        self.stay_alive = True

        # Sounder variables.
        self._sound_file: Optional[str] = None

        # Start main menu function running.
        self.run()

    def run(self) -> None:
        """
        Start running the main menu function.
        """

        if self.stay_alive:
            log.info("Starting application command menu.")

        while self.stay_alive:
            # Print a menu title.
            title_string = "   Sound Analyser   "
            self.app_io.app_out("=" * len(title_string))
            self.app_io.app_out(title_string)
            self.app_io.app_out("=" * len(title_string))

            # Print the menu for user selection.
            for key, value in MENU_ITEMS.items():
                self.app_io.app_out(f" <{key}> - {value}")

            # Get the user selection.
            self.app_io.app_out("\nMenu Selection : ", False)
            option = self.app_io.app_in()
            if option:
                option = option.strip()

            # Process user selection.
            if option == "1":
                self.record_sample()
                self.app_io.app_out("")
            elif option == "2":
                self.load_sample()
                self.app_io.app_out("")
            elif option == "3":
                self.play_sample()
            elif option == "4":
                self.analyse_sample()
            elif option == "5":
                self.stay_alive = False
                log.info("Stopping application command menu.")
            else:
                self.app_io.app_out("Invalid selection.")

    def record_sample(self) -> None:
        """
        Function to allow user to record a sound sample.
        The audio sample will be automatically saved with a
        file name that includes the current time.
        The filename is stored as the file for analysis
        via the appropriate menu option.
        """

        log.info("User selection to record sound sample.")

        # Calculate number of samples.
        num_samples = int(self._settings.sound.SAMPLE_RATE * self._settings.sound.SAMPLE_DUR)

        # Start recorder with the given values of
        # duration and sample frequency.
        # Note only recording 1 channel (the left) if more than 1 channel available.
        recording = sd.rec(num_samples, samplerate=self._settings.sound.SAMPLE_RATE, channels=1)

        # Record audio for the given number of seconds.
        sd.wait()

        # This will convert the NumPy array to an audio
        # file with the given sampling frequency.
        # Create the filename form the date and time.
        self._sound_file = f"sounder-{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"

        write(self._sound_file, self._settings.sound.SAMPLE_RATE, recording)

        # Plot the file.
        splot.plot_wav_file(self._sound_file, self._settings)

    def load_sample(self) -> None:
        """
        Function to allow user to load a previously recorded sound sample.
        The loaded sample waveform is displayed.
        The filename is stored as the file for analysis
        via the appropriate menu option.
        """

        log.info("User selection to load sound sample.")

        # Prompt the user for the sound sample to load.
        self.app_io.app_out("\nSound file : ", False)
        sound_file = self.app_io.app_in()
        if sound_file:
            self._sound_file = sound_file.strip()

            # Plot the file.
            splot.plot_wav_file(self._sound_file, self._settings)

    def play_sample(self) -> None:
        """
        Function to play (or replay) the previously recorded or loaded sound sample.
        """

        # Check if there is a file to play first.
        if self._sound_file:
            log.info(f"User selection to play sound sample: {self._sound_file}")

        # Read the sound file.
        try:
            sound_data, sample_rate = sf.read(self._sound_file)
        except FileNotFoundError:
            # Sound file could not be found; log a warning.
            log.warning(f"Error opening sound file: {self._sound_file}")
            return

        # Play the sound sample.
        sd.play(sound_data, sample_rate)
        sd.wait()

    def analyse_sample(self) -> None:
        """
        Function to analyse the previously recorded or loaded sound sample.
        """

        # Check if there is a file to analyse first.
        if self._sound_file:
            log.info(f"User selection to analyse sound sample: {self._sound_file}")

            # Perform sound analysis.
            # Only interested in section of the frequency spectrum for analysis.
            # In settings can nominate min/max depending on instrument.
            splot.analyse_wav_file(self._sound_file, self._settings)
        else:
            self.app_io.app_out("No sound file to analyse.", True)
