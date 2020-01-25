from tslearn.utils import to_time_series_dataset
import numpy as np
import os


def get_raw_dir_path(project_dir):
    return os.path.join(project_dir, "data", "raw")


def get_external_dir_path(project_dir):
    return os.path.join(project_dir, "data", "external")


def get_interim_dir_path(project_dir):
    return os.path.join(project_dir, "data", "interim")


def get_processed_dir_path(project_dir):
    return os.path.join(project_dir, "data", "processed")


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

