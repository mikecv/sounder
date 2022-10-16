"""
Functions to perform various plotting of sounder recordings.
"""

import logging
from math import ceil
from math import log10
from typing import Optional

import matplotlib.pyplot as plt  # type: ignore
from numpy import fft  # type: ignore
import numpy as np  # type: ignore
import scipy as sp  # type: ignore
from scipy.io import wavfile as wav  # type: ignore
from scipy.io.wavfile import read  # type: ignore

log = logging.getLogger(__name__)


def plot_wav_file(s_file: str, burn: int = 0) -> None:
    """
    Function to plot a sound sample - samples vs rel applitude.
    Option to burn starting samples to eliminate noise when
    recording starts.
    Args:
        s_file: Filename of the sound sample file to plot.
        burn:   Number of samples at start to burn (not Plot).
    """

    log.info(f"Plotting sound recording of file : {s_file}")

    # Specify plot size.
    plt.rcParams["figure.figsize"] = [8, 6]
    plt.rcParams["figure.autolayout"] = True

    # Read the sound file.
    sample_rate, sound_data = read(s_file)

    # Plot data.
    plt.plot(sound_data[burn:])

    # Set axis labels.4
    plt.ylabel("Amplitude")
    plt.xlabel("Samples")

    # Show plot.
    plt.show()


def analyse_wav_file(s_file: Optional[str], burn: int = 0) -> None:
    """
    Function to analyse a sound sample.
    Analysis is FFT so for best results want sound sample
    to be constant in the frequency domain.
    Args:
        s_file: Filename of the sound sample file to analyse.
        burn:   Number of samples at start to burn (not Plot).
    """

    log.info(f"Analysing sound recording of file : {s_file}")

    # Specify plot size.
    plt.rcParams["figure.figsize"] = [8, 6]
    plt.rcParams["figure.autolayout"] = True

    # Read the sound file.
    sample_rate, sound_data = read(s_file)

    # Convert sound array to float array.
    sound_data = sound_data / (2.0**15)

    # Burn samples at start of file if required.
    sample_data = sound_data[burn:]

    # Determine samples in the sound data.
    num_samps = len(sample_data)

    # Calculate FFT of the sample data.
    fft_data = fft.fft(sample_data)

    # Determine unique points, and elimiate negative space.
    num_unique_pts = ceil((num_samps + 1) / 2.0)
    fft_data = fft_data[0:num_unique_pts]
    fft_data = abs(fft_data)

    # Scale by number of points so that magnitude does not depend on duration
    # of the signal or sampling frequency.
    # And then square to get the power.
    fft_data = fft_data / float(num_samps)
    fft_data = fft_data**2

    # Multiply by 2 to ensure Nyquist frequency included.
    # Odd number of samples will not include Nyquist frequency.
    if num_samps % 2 > 0:
        fft_data[1 : len(fft_data)] = fft_data[1 : len(fft_data)] * 2
    else:
        fft_data[1 : len(fft_data) - 1] = fft_data[1 : len(fft_data) - 1] * 2

    # Compose the frequency array.
    freq_array = np.arange(0, num_unique_pts, 1.0) * (sample_rate / num_samps)

    # Compose frequency spectrum plot.
    plt.plot(freq_array, fft_data, color="k")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Not Power (dB)")

    plt.show()
