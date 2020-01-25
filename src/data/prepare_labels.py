import pandas as pd
import relevant_data
from datetime import timedelta
import numpy as np
import os
from pathlib import Path
import pickle
from scipy.signal import correlate
from tslearn.utils import to_time_series_dataset
import matplotlib.pyplot as plt


def get_failure_indicies(metadata):
    """Returns failure indicies"""
    return metadata[metadata.failure == 1].index.to_list()


def get_interim_dir_path(project_dir):
    return os.path.join(project_dir, "data", "02_intermediate")


def array_of_np_objects_to_collector(array):
    assert type(array) == np.ndarray, "argument type must be a numpy array"
    return list(array)


def to_same_length_time_series_dataset(data_collector):
    """Transforms data_collector containing arrays of different lengths 
    into a time series data with same length throught zero-padding"""
    X_ts = to_time_series_dataset(data_collector)
    X_ts[~np.isfinite(X_ts)] = 0  # nans are replaced with zeros
    X_ts = X_ts[:, :, 0]  # new shape
    return X_ts


def cross_correlation_normalized(x0, x1, coefficient=False):
    """ Returns normalized cross-correlation of two 1D timeseries.
    Returned values lie in [0,1], where 0 indicates no correlation
    and 1 indicates full correlation.    
    If coefficient ist set to False, returns entire cross correlation
    vector, otherwise returns maximum."""
    a = np.dot(abs(x0), abs(x1))
    b = np.correlate(x0, x1, "full")
    c = b / a
    if coefficient:
        return np.max(c)
    return c


def cross_corr(X_ts, metadata):
    """
    Computes cross-correlation between X_ts[i] and X_ts[f],
    where X_ts[f] is the time series representing a failure in a seqeunce
    of successive timeseries (without failure)  

    Parameters
    ----------
    X_ts : 2d-array with shape (n_samples, n_timestamps)
        Dataset of time series.
    metadata : pandas.DataFrame
        Contains all descriptive information about the time series' sequence.

    Returns
    -------    
    Array max values of cross-correlations between timeseries X_ts[i] and X_ts[f].

    """
    failures_i = get_failure_indicies(metadata)
    cross_corr_list = []
    first = 0
    for i in failures_i:
        for j in range(first, i):
            # cross_corr = np.max(np.correlate(X_load[i],X_load[j]),"full")
            cross_corr = cross_correlation_normalized(X_ts[j], X_ts[i], True)
            cross_corr_list.append(cross_corr)
        j = i
        cross_corr = cross_correlation_normalized(X_ts[j], X_ts[i], True)
        cross_corr_list.append(cross_corr)
        first = i + 1

    return np.array(cross_corr_list)


def create_labels_from_metadata(metadata):
    """
    Create labels linearly using failure indicies.

    Parameters
    ----------
    metadata : pandas.DataFrame
        Contains all descriptive information about the time series' sequence.

    Returns
    -------
    Array containing labels.

    """
    # get failure indicies
    failures_i = get_failure_indicies(metadata)
    # create labels linearly
    labels = []
    first = 0
    for i in failures_i:
        if first == 0:
            num_points = i - first + 1
            labels_subsequence = np.linspace(0, 1, num=num_points).tolist()
        else:
            num_points = i - first
            labels_subsequence = np.linspace(0, 1, num=num_points).tolist()
        labels.extend(labels_subsequence)
        first = i
    # last timeseries' subsequence is treated seperately
    num_points = len(metadata) - 1 - failures_i[-1]
    labels_subsequence = np.linspace(0, 1, num=num_points).tolist()
    labels.extend(labels_subsequence)
    return np.array(labels)


def main(project_dir):
    # get path
    interim_dir_path = get_interim_dir_path(project_dir)

    # load data from interim_dir_path as collectors
    loaded = np.load(os.path.join(interim_dir_path, "data.npz"), allow_pickle=True)
    collector_load = array_of_np_objects_to_collector(loaded["load"])
    collector_speed = array_of_np_objects_to_collector(loaded["speed"])
    metadata = pd.read_pickle(os.path.join(interim_dir_path, "metadata"))

    # transform collectors into timeseries
    X_load = to_same_length_time_series_dataset(collector_load)
    X_speed = to_same_length_time_series_dataset(collector_speed)

    # create labels
    labels_linear = create_labels_from_metadata(metadata)

    return labels_linear


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    main(project_dir)
    # save labels
    np.save(os.path.join(interim_dir_path, "labels_linear"), labels_linear)

# project_dir = "/home/adnene33/Documents/FM/Tool-Wear-Classification"

