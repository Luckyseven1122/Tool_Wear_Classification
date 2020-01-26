import utils
import os
import numpy as np
from prepare_labels import cross_correlation_normalized
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt

def autocorr(x):
    result = numpy.correlate(x, x, mode='full')
    return result[result.size/2:]

def autocorrelation_normalized(arr):
    """
    Computes the auto_correlation function of the input time series
    
    Parameters
    ----------
    arr : 1d numpy array
        1d time series.

    Returns
    -------
    autocorr : 1d numpy array
        Normalized auto-correlation function of arr.

    """
    a = np.dot(abs(arr), abs(arr))
    b = np.correlate(arr, arr, "full")
    autocorr = b / a
    return autocorr

def to_autocorrelation_dataset(X_ts):
    """
    Computes the autocorrelation functions of the input time series of Dataset at each row.

    Parameters
    ----------
    X_ts : TYPE
        DESCRIPTION.

    Returns
    -------
    X_ts_autocorr : 2d numpy array
       Autocorrelation dataset.

    """
    X_ts_autocorr = np.apply_along_axis(func1d=autocorrelation_normalized, axis=1, arr=X_ts)
    return X_ts_autocorr
    

def main():
    interim_dir_path = utils.get_external_dir_path(project_dir)
    loaded = np.load(os.path.join(interim_dir_path, "data.npz"), allow_pickle=True)
    collector_load = utils.array_of_np_objects_to_collector(loaded["load"])
    collector_speed = utils.array_of_np_objects_to_collector(loaded["speed"])

    X_load = utils.to_same_length_time_series_dataset(collector_load)
    X_speed = utils.to_same_length_time_series_dataset(collector_speed)
    
    X_load_auto_corr = np.apply_along_axis(cross_correlation_normalized, axis=0, X_load, )
    x0 = X_load[0]
    x0_autocorr = acf(x0, nlags=40, fft=True)


    x0_autocorr_mine = autocorrelation_normalized(x0)
    X_load_autocor = np.apply_along_axis(func1d=autocorrelation_normalized, axis=1, arr=X_load)
    pass


if __name__ == "__main__":
    main()
    pass
