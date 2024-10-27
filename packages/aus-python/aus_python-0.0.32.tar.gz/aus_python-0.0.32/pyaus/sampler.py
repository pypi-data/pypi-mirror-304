"""
File: sampler.py
Author: Jeff Martin
Date: 1/26/23

This file contains functionality for processing audio files for use with samplers.
"""

import os
import numpy as np
from . import audiofile
import pedalboard as pb


class Sample(audiofile.AudioFile):
    def __init__(self, audio, sample_rate=44100, path=""):
        """
        Creates a Sample with provided audio
        :param audio: A NumPy array of audio samples
        :param sample_rate: The sample rate of the audio
        :param path: The path of the audio file
        """
        super().__init__(frames=audio.shape[-1], duration=audio.shape[-1] / sample_rate, num_channels=1, sample_rate=sample_rate)
        self.samples = audio
        self.path = path
        if path != "":
            self.file_name = os.path.split(path)[-1]
        else:
            self.file_name = ""
        self.analysis = {}
        self.dynamic_name = None
        self.dynamic_id = None
        self.instrument_name = None
        self.midi = None
        self.pitched = False
        self.string_name = None
        self.string_id = None


def extract_samples(audio: audiofile.AudioFile, amplitude_regions: list, pre_frames_to_include: int = 0, 
                    post_frames_to_include: int = 0, pre_envelope_type="hanning", pre_envelope_frames: int = 20,
                    post_envelope_type="hanning", post_envelope_frames: int = 20) -> list:
    """
    Extracts samples from an AudioFile.
    
    :param audio: An AudioFile object
    :param amplitude_regions: A list of amplitude regions from the identify_amplitude_regions function
    :param pre_frames_to_include: If this is set to greater than 0, the sample will be extended backward
    to include these additional frames. This is useful for ensuring a clean sample onset.
    :param post_frames_to_include: If this is set to greater than 0, the sample will be extended forward
    to include these additional frames. This is useful for ensuring a clean sample release.
    :param pre_envelope_type: The envelope type to apply to the beginning of the sound, for a clean onset.
    Supported envelope types are Bartlett, Blackman, Hamming, and Hanning.
    :param pre_envelope_frames: The duration in frames of the pre envelope
    :param post_envelope_type: The envelope type to apply to the end of the sound, for a clean release.
    Supported envelope types are Bartlett, Blackman, Hamming, and Hanning.
    :param post_envelope_frames: The duration in frames of the post envelope
    
    :return: A list of AudioFile objects with the samples
    """
    file_samples = np.hstack((
        np.zeros((audio.num_channels, pre_frames_to_include), dtype=audio.samples.dtype),
        audio.samples,
        np.zeros((audio.num_channels, post_frames_to_include), dtype=audio.samples.dtype)
    ))
    samples = []

    # Adjust the samples to include frames before and after
    for i, region in enumerate(amplitude_regions):
        amplitude_regions[i] = (
            region[0],
            region[1] + pre_frames_to_include + post_frames_to_include
        )

    # Create the samples
    for sample in amplitude_regions:
        new_audio_file = audiofile.AudioFile(
            audio_format=audio.audio_format,
            bits_per_sample=audio.bits_per_sample,
            block_align=audio.block_align,
            byte_rate=audio.byte_rate,
            bytes_per_sample=audio.bytes_per_sample,
            duration=(sample[1] - sample[0] + 1) / audio.sample_rate,
            num_channels=audio.num_channels,
            frames=(sample[1] - sample[0] + 1),
            sample_rate=audio.sample_rate
        )
        new_audio_file.samples = file_samples[:, sample[0]:sample[1]+1]

        # Get the windows
        pre_envelope = None
        if pre_envelope_type == "bartlett":
            pre_envelope = np.bartlett(pre_envelope_frames * 2)[:pre_envelope_frames]
        elif pre_envelope_type == "blackman":
            pre_envelope = np.blackman(pre_envelope_frames * 2)[:pre_envelope_frames]
        elif pre_envelope_type == "hanning":
            pre_envelope = np.hanning(pre_envelope_frames * 2)[:pre_envelope_frames]
        elif pre_envelope_type == "hamming":
            pre_envelope = np.hamming(pre_envelope_frames * 2)[:pre_envelope_frames]
        post_envelope = None
        if post_envelope_type == "bartlett":
            post_envelope = np.bartlett(post_envelope_frames * 2)[post_envelope_frames:]
        elif post_envelope_type == "blackman":
            post_envelope = np.blackman(post_envelope_frames * 2)[post_envelope_frames:]
        elif post_envelope_type == "hanning":
            post_envelope = np.hanning(post_envelope_frames * 2)[post_envelope_frames:]
        elif post_envelope_type == "hamming":
            post_envelope = np.hamming(post_envelope_frames * 2)[post_envelope_frames:]
        
        # Apply the windows
        if pre_envelope is not None:
            for i in range(pre_envelope_frames):
                for j in range(new_audio_file.num_channels):
                    new_audio_file.samples[j, i] *= pre_envelope[i]
        if post_envelope is not None:
            for i in range(post_envelope_frames):
                for j in range(new_audio_file.num_channels):
                    new_audio_file.samples[j, new_audio_file.frames - post_envelope_frames + i] *= post_envelope[i]

        samples.append(new_audio_file)
    
    return samples


def identify_amplitude_regions(audio: audiofile.AudioFile, level_delimiter: float = -30, scale_level_delimiter: bool = True, 
                               num_consecutive: int = 10, channel_index: int = 0) -> list:
    """
    Identifies amplitude regions in a sound. You provide a threshold, and any time the threshold is
    breached, we start a new amplitude region which ends when we return below the threshold. This is
    useful for pulling out individual samples from a file that has multiple samples in it.

    :param audio: An AudioFile object
    :param level_delimiter: The lowest level (dBFS) allowed in a region. This will be scaled by the maximum amplitude
    in the audio file channel that is being analyzed, unless that feature is turned off by the next parameter. 
    :param scale_level_delimiter: Whether or not to scale the level delimiter by the maximum amplitude in
    the audio file channel that is being analyzed
    :param num_consecutive: The number of consecutive samples below the threshold required to end a region.
    Note that these samples will not be included in the amplitude region; they will only be used to determine
    if an amplitude region is ending.
    :param channel_index: The index of the channel in the AudioFile to study
    
    :return: A list of tuples. Each tuple contains the starting and ending frame index of an amplitude region.
    """
    regions = []
    current_region = None
    num_below_threshold = 0
    last_above_threshold = 0

    if audio.frames > 0:
        # Scale the level delimiter by the maximum amplitude in the audio file
        if scale_level_delimiter:
            maxval = 20 * np.log10(np.max(np.abs(audio.samples[channel_index, :])))
            level_delimiter = maxval + level_delimiter
        
        for i in range(audio.frames):
            if 20 * np.log10(np.abs(audio.samples[channel_index, i])) >= level_delimiter:
                last_above_threshold = i
                num_below_threshold = 0
                if current_region is None:
                    current_region = i
            else:
                num_below_threshold += 1
                if current_region is not None and num_below_threshold >= num_consecutive:
                    regions.append((current_region, last_above_threshold))
                    current_region = None

        if current_region is not None:
            regions.append((current_region, audio.frames - 1))

    return regions


def detect_peaks(audio: audiofile.AudioFile, channel_index: int = 0) -> list:
    """
    Detects peaks in an audio file. A peak is located at a sample N where the waveform changes direction.
    :param audio: An AudioFile object with the contents of a WAV file
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of indices; each index corresponds to a frame with a peak in the selected channel.
    """
    peaks = []
    for i in range(1, audio.frames - 1):
        if audio.samples[channel_index, i-1] < audio.samples[channel_index, i] > audio.samples[channel_index, i+1] \
            and audio.samples[channel_index, i] > 0:
            peaks.append(i)
        elif audio.samples[channel_index, i-1] > audio.samples[channel_index, i] < audio.samples[channel_index, i+1] \
            and audio.samples[channel_index, i] < 0:
            peaks.append(i)
    return peaks


def fit_amplitude_envelope(audio: audiofile.AudioFile, chunk_width: int = 5000, channel_index: int = 0) -> list:
    """
    Fits an amplitude envelope to a provided audio file.
    Detects peaks in an audio file. Peaks are identified by being surrounded by lower absolute values to either side.
    :param audio: An AudioFile object with the contents of a WAV file
    :param chunk_width: The AudioFile is segmented into adjacent chunks, and we look for the highest peak amplitude 
    in each chunk.
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of tuples; the tuple has an index and an amplitude value.
    """
    envelope = []
    for i in range(0, audio.frames, chunk_width):
        peak_idx = np.argmax(np.abs(audio.samples[channel_index, i:i+chunk_width]))
        envelope.append((i + peak_idx, np.abs(audio.samples[channel_index, i + peak_idx])))
    return envelope


def detect_major_peaks(audio: audiofile.AudioFile, min_percentage_of_max: float = 0.9, chunk_width: int = 5000, channel_index: int = 0) -> list:
    """
    Detects major peaks in an audio file. A major peak is a sample peak that is one of the highest in its "local region."
    This is useful for identifying the period length (and therefore the fundamental frequency) of audio with a strong
    first harmonic, since the first harmonic will create the highest peak of the waveform. It will not
    work very well on Gaussian noise or audio with a very weak fundamental.
    
    The "local region" is specified by the chunk width. We segment the audio file into C segments of width chunk_width,
    and search for the highest peak P in that chunk. Then we identify all other peaks that are close in height
    to the highest peak P. A peak is close in height to said peak P if it is greater than or equal to min_percentage_of_max
    of that peak. (For example, suppose the highest peak is 1, and the min_percentage_of_max is 0.9. Then any peak with
    amplitude from 0.9 to 1 will be considered a major peak.)
    
    :param audio: An AudioFile object with the contents of a WAV file
    :param min_percentage_of_max: A peak must be at least this percentage of the maximum peak to be included as a major
    peak.
    :param chunk_width: The width of the chunk to search for the highest peak
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of tuples; the tuple has an index and an amplitude value.
    """
    peaks = []
    for i in range(1, audio.frames - 1, chunk_width):
        # Get the index and absolute value of the highest peak in the current chunk
        peak_idx = i + np.argmax(audio.samples[channel_index, i:i+chunk_width])
        peak_val = audio.samples[channel_index, peak_idx]
        
        # print(peak_idx, peak_val)

        # Iterate through the current chunk and find all major peaks
        j = i
        while j < i + chunk_width and j < audio.frames - 1:
            if (
                # If the current sample is a positive peak (both neighboring samples are lower)
                (audio.samples[channel_index, j-1] < audio.samples[channel_index, j] > audio.samples[channel_index, j+1] \
                    and audio.samples[channel_index, j] > 0) \
                
                # And the peak is a major peak
                and audio.samples[channel_index, j] >= peak_val * min_percentage_of_max
            ):
                peaks.append((j, audio.samples[channel_index, j]))
            j += 1

    return peaks


def detect_loop_points(audio: audiofile.AudioFile, channel_index: int = 0, num_periods: int = 5, effective_zero: float = 0.001, 
                       maximum_amplitude_variance: float = 0.1, sample_amplitude_level_boundary: float = 0.1, 
                       loop_left_padding: int=100, loop_right_padding: int=100) -> list:
    """
    Detects loop points in an audio sample. Loop points are frame indices that could be used for
    a seamless repeating loop in a sampler. Ideally, if you choose loop points correctly, no crossfading
    would be needed within the loop.

    We have several requirements for a good loop:
    1. The standard deviation of peak amplitudes should be minimized (i.e. the loop is not increasing or decreasing in amplitude)
    2. The distance between successive wave major peaks should be consistent (i.e. we are looking for periodic waveforms)
    3. The frames at which looping begins and ends should have values as close to 0 as possible (we want to avoid clicks)
    
    :param audio: An AudioFile object
    :param channel_index: The index of the channel to scan for loops (you really should use mono audio 
    with a sampler)
    :param num_periods: The number of periods to include from the waveform
    :param effective_zero: The threshold below which we just consider the amplitude to be 0. This is assumed to be a 
    floating-point value between 0 (no amplitude) and 1 (max amplitude). If your file is fixed format, this will be 
    automatically scaled.
    :param maximum_amplitude_variance: The maximum percentage difference between the biggest and 
    smallest major peak in the loop
    :param sample_amplitude_level_boundary: Used to determine where the sample sits in the provided audio file. This is useful
    because we don't want to detect loop points in just any region of the sample - the loop points should have a similar dynamic
    level to the rest of the sample.
    :param loop_left_padding: The number of frames to ignore at the start of the amplitude region. This is needed to keep the loop
    from being in the attack portion of the sound.
    :param loop_right_padding: The number of frames to ignore at the end of the amplitude region. This is needed to keep the loop
    from being too close to the decay portion of the sound.
    
    :return: A list of tuples that are start and ending frames for looping
    """

    # The audio file amplitude level ranges
    amplitude_level_ranges = identify_amplitude_regions(audio, sample_amplitude_level_boundary, 10, channel_index)

    if len(amplitude_level_ranges) < 1:
        return []
    else:
        # combine the amplitude level ranges
        amplitude_level_range = (amplitude_level_ranges[0][0], amplitude_level_ranges[-1][-1])

        # If we are dealing with a fixed (int) file, we need to adjust the effective zero because
        # the samples are integers, not floating point values.
        if type(audio.samples[0, 0]) == np.int16 \
            or type(audio.samples[0, 0]) == np.int32 \
            or type(audio.samples[0, 0]) == np.int64: 
            effective_zero = int(effective_zero * 2 ** (audio.bits_per_sample - 1))
            sample_amplitude_level_boundary = int(sample_amplitude_level_boundary * 2 ** (audio.bits_per_sample - 1))

        # The major peaks in the sound file.
        major_peaks = detect_major_peaks(audio, 0.9, 5000, channel_index)
        
        # This stores frame tuples that identify potential loop points.
        frame_tuples = []

        # We will try to build a loop starting at each peak, then shifting backward to a zero point.
        for i in range(len(major_peaks)):
            potential_loop_peaks = []
            
            # We will use these two valuse to determine if there is too much dynamic variation
            # within the proposed loop.
            max_peak = -np.inf  # the absolute value of the major peak with greatest magnitude
            min_peak = np.inf  # the absolute value of the major peak with least magnitude
        
            # We start by grabbing peaks for the minimum number of periods necessary. We have to 
            # grab an extra peak to complete the final period.
            for j in range(i, min(i + num_periods + 1, len(major_peaks))):
                potential_loop_peaks.append(major_peaks[j])
                peak_abs = np.abs(major_peaks[j][1])
                if peak_abs > max_peak:
                    max_peak = peak_abs
                if peak_abs < min_peak:
                    min_peak = peak_abs
            
            # If we weren't able to pull enough periods, we can't continue with making the loop.
            if len(potential_loop_peaks) < num_periods:
                break

            # If there's too much dynamic variation in this audio chunk, we can't continue with
            # making the loop. We want loops that have a steady sound, rather than fluctuating
            # wildly in dynamic level.
            if (max_peak - min_peak) / max_peak > maximum_amplitude_variance:
                continue

            # We need to record loop points now. Recall that the final peak is actually the beginning
            # of the next period, so we need to move back one sample.
            loop_points = [potential_loop_peaks[0][0], potential_loop_peaks[-1][0] - 1]
            period_width = (loop_points[1] - loop_points[0]) // num_periods

            # Now we shift back to make the loop start and end on 0. There might be multiple possible
            # places where the loop could start and end on 0.
            while loop_points[0] + period_width > potential_loop_peaks[0][0] and loop_points[0] >= 0:
                loop_points[0] -= 1
                loop_points[1] -= 1

                # If we've found good loop points, we will record them. They must match the following criteria:
                # 1. Start and end at the effective zero level (to avoid clicks)
                # 2. Be located within the amplitude level range that was identified earlier (to avoid identifying
                #    loop points within the attack or decay portions of the sample)
                if np.abs(audio.samples[channel_index, loop_points[0]]) < effective_zero \
                    and np.abs(audio.samples[channel_index, loop_points[1]]) < effective_zero:
                    if loop_points[0] >= amplitude_level_range[0] + loop_left_padding \
                        and loop_points[1] <= amplitude_level_range[1] - loop_right_padding:
                        frame_tuples.append((loop_points[0], loop_points[1]))
                    break

        return frame_tuples


def load_samples(directory, iowa=False) -> list:
    """
    Loads preprocessed samples from a directory, and returns them as a list of Samples
    :param directory: The directory to search
    :param iowa: Whether or not to add additional information from the file name for 
    Iowa EMS samples
    :return: A list of Samples
    """
    samples = []
    files = audiofile.find_files(directory)
    for file in files:
        with pb.io.AudioFile(file, "r") as a:
            audio = a.read(a.frames)
            sample = Sample(np.reshape(audio, (audio.size)), a.samplerate, file)
            if iowa:
                name_data = os.path.split(file)[-1].split('.')
                sample.midi = int(name_data[1])
                sample.instrument_name = name_data[2]
                sample.dynamic_name = name_data[5]
                sample.pitched = True
                sample.string_name = name_data[4][-1]
            samples.append(sample)
    return samples
