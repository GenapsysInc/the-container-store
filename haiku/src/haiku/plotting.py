"""
Plotting utilities
"""
import logging

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks

logger = logging.getLogger(__name__)


def heatmap2d(arr: np.ndarray, fname: str = None, vmin: int = None, vmax: int = None, dpi: int = 300):
    plt.clf()
    logger.info("Generating Heatmap")
    plt.imshow(arr, cmap='viridis', vmin=vmin, vmax=vmax)
    plt.colorbar()
    if fname:
        plt.savefig(str(fname) + ".png", format="png", dpi=dpi)
    plt.clf()


def histogram(arr: np.ndarray, fname: str = None, bins: int = 100, hist_range=None, dpi: int = 300, with_peak=False):

    plt.clf()
    logger.info("Generating Histogram")
    hist = plt.hist(arr, bins=bins, range=hist_range)
    max_height = hist[0][np.argmax(hist[0])]
    if with_peak:
        peak_indices, _ = find_peaks(hist[0], prominence=max_height * 0.25, height=max_height * 0.5)
        for idx in peak_indices:
            plt.axvline(hist[1][idx], color='r')
    if fname:
        plt.gcf().savefig(str(fname) + ".png", format="png", dpi=dpi)
    plt.clf()
    return hist


def plot_peaks(x, y, fname: str = None, dpi: int = 300):
    plt.clf()
    logger.info("Generating Plot Peak")
    loc_max = argrelextrema(y, np.greater)
    loc_max = np.asarray(loc_max)
    main_peaks = []
    for i in range(loc_max.shape[1]):
        if y[loc_max[0][i]] > 1000000:
            main_peaks.append(x[loc_max[0][i]])
    plt.plot(x, y, c='g')
    for peak in main_peaks:
        logger.debug('%.4f' % peak)
        plt.axvline(x=peak, color='r')
    if fname:
        plt.gcf().savefig(str(fname) + ".png", format="png", dpi=dpi)
    main_peaks = np.asarray(main_peaks)
    return main_peaks


def hist_to_scatter_reducer(hist):
    x = []
    y = []
    for i in range(len(hist[0])):
        if hist[0][i] != 0:
            x.append((hist[1][i+1] + hist[1][i])/2)
            y.append(hist[0][i])
    x = np.asarray(x)
    y = np.asarray(y)
    return x, y
