"""
Functions to perform various plotting of sounder recordings.
"""

import logging
from math import ceil
from math import log10
from typing import Optional

import dotsi  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from numpy import fft  # type: ignore
import numpy as np  # type: ignore
from scipy.io import wavfile as wav  # type: ignore
from scipy.io.wavfile import read  # type: ignore

log = logging.getLogger(__name__)


def plot_wav_file(s_file: str, settings: dotsi.Dict) -> None:
    """
    Function to plot a sound sample - samples vs rel applitude.
    Option to burn starting samples to eliminate noise when
    recording starts.
    Args:
        settings:   Application settings.
        burn:       Number of samples at start to burn (not Plot).
    """

    log.info(f"Plotting sound recording of file: {s_file}")

    # Specify plot size.
    plt.rcParams["figure.figsize"] = [settings.sound.FIG_X_SIZE, settings.sound.FIG_Y_SIZE]
    plt.rcParams["figure.autolayout"] = True

    # Read the sound file.
    try:
        sample_rate, sound_data = read(s_file)
    except FileNotFoundError:
        # Sound file could not be found; log a warning.
        log.warning(f"Error opening sound file: {s_file}")
        return

    # Calculate seconds to burn (if any).
    burn_samples = int(settings.sound.BURN_SECS * settings.sound.SAMPLE_RATE)

    # Plot data.
    plt.plot(sound_data[burn_samples:], linewidth=0.5, color="blue")

    # Set axis labels.
    plt.ylabel("Amplitude")
    plt.xlabel("Samples")

    # Show plot.
    plt.show()


def analyse_wav_file(s_file: Optional[str], settings: dotsi.Dict) -> None:
    """
    Function to analyse a sound sample.
    Analysis is FFT so for best results want sound sample
    to be constant in the frequency domain.
    Args:
        s_file      : Filename of the sound sample file to analyse.
        settings:   Application settings.
    """

    log.info(f"Analysing sound recording of file: {s_file}")

    # Specify plot details.
    # Create 2 plots - the main frequency spectrum plot at the bottom,
    # and a smaller plot at the top with annotations and lines to show
    # where musical notes lie.
    #
    # Set the plots to use the same x axis.
    # The x axis will only be shown on the spectrum plot, and the
    # annotations plot will not show any axis marks as not necessary.
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, height_ratios=[1, 5])
    fig.figsize = (settings.sound.FIG_X_SIZE, settings.sound.FIG_Y_SIZE)
    fig.autolayout = True
    ax2.set_facecolor("#c8c8c8")

    # Read the sound file.
    sample_rate, sound_data = read(s_file)

    # Convert sound array to float array.
    sound_data = sound_data / (2.0**15)

    # Burn samples at start of file if required.
    # Calculate seconds to burn (if any).
    burn_samples = int(settings.sound.BURN_SECS * settings.sound.SAMPLE_RATE)
    sample_data = sound_data[burn_samples:]

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
    # First change fft data to array of power values.
    power = np.array([None] * len(freq_array))
    for idx in range(len(freq_array)):
        power[idx] = 10.0 * log10(fft_data[idx])

    # Only show portion of the frequency spectrum we're interest in.
    lower_freq = int(settings.sound.FFT_MIN_HZ * num_unique_pts / settings.sound.SAMPLE_RATE * 2)
    upper_freq = int(settings.sound.FFT_MAX_HZ * num_unique_pts / settings.sound.SAMPLE_RATE * 2)

    # Plot the frequecy spectrum.
    ax2.plot(freq_array[lower_freq:upper_freq], power[lower_freq:upper_freq], linewidth=0.5, color="cyan", zorder=10)

    # Add axis ticks.
    # Do fixed number of ticks, not fixed intervals.
    tick_interval = (freq_array[upper_freq] - freq_array[lower_freq]) / (settings.sound.PLOT_X_TICKS - 1)
    tick_interval = ceil(tick_interval / settings.sound.PLOT_TICK_RES) * settings.sound.PLOT_TICK_RES
    plt.xticks(np.arange(freq_array[lower_freq], freq_array[upper_freq], tick_interval))

    # Plot the moving average of the freq spectrum.
    window = np.ones(settings.sound.FFT_AVG_WIN) / settings.sound.FFT_AVG_WIN
    moving_average = np.convolve(power[lower_freq:upper_freq], window, "same")
    ax2.plot(freq_array[lower_freq:upper_freq], moving_average, linewidth=1, color="black", zorder=20)

    # Add the note annotations line to the spectrum plot as well (as to the top plot).
    ax2.axvline(440, linewidth=1, color="red", linestyle="dotted", zorder=0)

    # Plot the note lines and annotations on the top plot.
    # This plot will have an arbitrary 0-1 y axis range, but markers will not be shown.

    # Calculate array of A notes to annotate.
    a_notes = [27.5]
    for idx in range(1, 7):
        a_notes.append(a_notes[idx - 1] * 2)
    ax1.set_ylim([0, 1])
    ax1.axis("off")
    for note in a_notes:
        ax1.axvline(note, linewidth=1, color="red", linestyle="dotted", zorder=0)
        ax1.text(
            note,
            1.0,
            "A",
            color="red",
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round",
                ec=(1.0, 0.5, 0.5),
                fc=(1.0, 0.8, 0.8),
            ),
        )

    # Add axis labels.
    # Only need labels for the spectrum plot (lower plot).
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Power (dB)")

    plt.show()
