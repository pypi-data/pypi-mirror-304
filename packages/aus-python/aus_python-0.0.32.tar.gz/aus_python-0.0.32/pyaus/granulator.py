"""
File: granulator.py
Author: Jeff Martin
Date: 7/16/23

This file is for experimenting with granular synthesis.
"""

import numpy as np
import random

np.seterr(divide="ignore")
_rng = random.Random()
 

def extract_grain(audio: np.ndarray, start_point=None, grain_size=None, window="hanning", max_window_size=None) -> np.ndarray:
    """
    Extracts a single grain from an array of samples.
    :param audio: A numpy array of audio samples
    :param start_point: The starting frame of the grain. If None, this will be randomly chosen.
    :param grain_size: The size of the grain in frames. If None, this will be randomly chosen.
    :param window: The window that will be applied to the grain.
    :param max_window_size: If specified, the window will not be larger than this size. If the grain is longer,
    the window will be split and only applied to the start and end of the grain.
    :return: A Numpy array with the grain
    """
    if audio is None:
        raise TypeError("You need to provide audio to granulate.")
    else:
        if start_point is None:
            start_point = _rng.randint(0, audio.shape[0] - 1)
        if grain_size is None:
            grain_size = _rng.randint(0, audio.shape[0] - 1 - start_point)
        if max_window_size is None:
            max_window_size = grain_size
        elif max_window_size > grain_size:
            max_window_size = grain_size
        grain = audio[:, start_point:start_point + grain_size]
        if window == "bartlett":
            window = np.bartlett(max_window_size)
        elif window == "blackman":
            window = np.blackman(max_window_size)
        elif window == "hanning":
            window = np.hanning(max_window_size)
        elif window == "hamming":
            window = np.hamming(max_window_size)
        else:
            window = np.ones((max_window_size))
        
        if max_window_size < grain_size:
            window = np.hstack((window[:max_window_size // 2], np.ones((grain_size - max_window_size)), window[max_window_size // 2:]))
        
        return grain * window
    

def find_max_grain_dbfs(grains: list):
    """
    Finds the maximum overall dbfs (by grain) of a list of grains. Useful
    for getting rid of grains with a low dbfs.
    :param grains: A list of grains
    :return: The dbfs of the grain with the loudest dbfs
    """
    max_dbfs = -np.inf
    for grain in grains:
        try:
            rms = np.sqrt(np.average(np.square(grain.samples), axis=grain.samples.ndim-1))
            dbfs = 20 * np.log10(np.abs(rms))
            max_dbfs = max(max_dbfs, dbfs)
        except Exception:
            pass
    return max_dbfs


def merge_grains(grains: list, overlap_size=10) -> np.ndarray:
    """
    Merges a list of grains, with some overlap between grains
    :param grains: A list of grains
    :param overlap_size: The number of samples to overlap from grain to grain
    :return: An array with the combined grains
    """
    current_grain = 1
    output = grains[0].samples
    while current_grain < len(grains):
        output = np.hstack((output[:-overlap_size], output[-overlap_size:] + grains[current_grain].samples[:overlap_size], grains[current_grain].samples[overlap_size:]))
        current_grain += 1
    return output


def scale_grain_peaks(grains: list):
    """
    Scales the peaks of a list of grains so they all have the same peak amplitude.
    The grains will be scaled in place.
    :param grains: The list of grains
    """
    maxamp = 0
    for grain in grains:
        maxamp = max(maxamp, np.max(grain.samples))
    for i in range(len(grains)):
        grains[i].samples /= maxamp
