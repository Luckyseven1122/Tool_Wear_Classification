import pandas as pd
import relevant_data
from datetime import timedelta
import numpy as np
import os
from pathlib import Path
import utils


def create_metadata(timestamps_collector, length, duration, offset=0):
    """Returns DataFrame containing begin and end timestamps, duration 
    and length of each process in the sequence"""

    begin_end_dict = {"begin": [], "end": [], "duration": [], "length": []}
    for i in range(len(timestamps_collector)):
        begin, end = timestamps_collector[i][0], timestamps_collector[i][-1]
        begin = pd.to_datetime(begin, infer_datetime_format=True) + timedelta(
            hours=offset
        )
        end = pd.to_datetime(end, infer_datetime_format=True) + timedelta(hours=offset)
        begin_end_dict["begin"].append(begin)
        begin_end_dict["end"].append(end)
        begin_end_dict["duration"].append(duration[i])
        begin_end_dict["length"].append(length[i])
        df_metadata = pd.DataFrame.from_dict(begin_end_dict)
    return df_metadata


def read_raw_from_file(file_path, machine_name):
    """ Reads a single raw data file in /01_raw and returns load, 
    speed and timestamps and its corresponding metadata"""

    df = pd.read_pickle(file_path, compression="infer")
    index_machine = df.index[df["machine_name"] == machine_name].tolist()[0]

    # load data from influx-database-collector
    load_collector = df.loc[index_machine, "load_collector"]
    speed_collector = df.loc[index_machine, "speed_collector"]
    timestamps_collector = df.loc[index_machine, "time_stamps_collector"]

    beg_ind_speed = df.loc[index_machine, "beg_ind_speed"]
    end_ind_speed = df.loc[index_machine, "end_ind_speed"]

    length = end_ind_speed - beg_ind_speed

    f_sample = 100  # Hz
    t_sample = 1 / f_sample
    duration = t_sample * length

    # creates an informative DataFrame corresponding to a sequence of processes
    df_metadata = create_metadata(timestamps_collector, length, duration, offset=1)
    return load_collector, speed_collector, df_metadata


def read_all_raw_files():
    """Reads all raw data files in /01_raw"""
    pass


def main(project_dir, machine_name):
    """ Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed)."""

    raw_dir_path = os.path.join(project_dir, "data", "raw")

    filenames = [
        f
        for f in os.listdir(raw_dir_path)
        if os.path.isfile(os.path.join(raw_dir_path, f))
    ][1:]
    filenames.sort()
    print(filenames)

    # get relevant processes to extract
    relevance_dict = relevant_data.relevance_dict
    failure_index_dict = relevant_data.failure_index_dict

    # create dictionaries to store data being read
    meta_dict = {
        "begin": [],
        "end": [],
        "length": [],
        "duration": [],
        "vollnut": [],
        "failure": [],
    }
    data_dict = {"load_collector": [], "speed_collector": []}

    for filename in filenames:
        file_path = os.path.join(raw_dir_path, filename)
        print(">>> reading {}...".format(filename))
        load_collector, speed_collector, df_metadata = read_raw_from_file(
            file_path, machine_name
        )

        indicies = relevance_dict[filename]["relevant_processes_i"]
        vollnut = relevance_dict[filename]["vollnut"]

        # extract relevant timeseries
        load_collector = [load_collector[i] for i in indicies]
        speed_collector = [speed_collector[i] for i in indicies]

        # extract corresponding relevant metadata
        df_metadata = df_metadata.iloc[indicies]

        # add failure column to metadata
        df_metadata["failure"] = np.zeros(shape=(len(df_metadata)), dtype=int)
        failure_indicies = failure_index_dict[filename]
        df_metadata.loc[failure_indicies, "failure"] = 1

        # add vollnut column to metadata
        df_metadata["vollnut"] = vollnut

        print(">>> appending current data to full dataset...")

        # append extracted load and speed to data dictionary
        data_dict["load_collector"].extend(load_collector)
        data_dict["speed_collector"].extend(load_collector)

        # append extracted metadata to metadata dictionary
        current_meta_dict = df_metadata.to_dict(orient="list")
        meta_dict["begin"].extend(current_meta_dict["begin"])
        meta_dict["end"].extend(current_meta_dict["end"])
        meta_dict["length"].extend(current_meta_dict["length"])
        meta_dict["duration"].extend(current_meta_dict["duration"])
        meta_dict["vollnut"].extend(current_meta_dict["vollnut"])
        meta_dict["failure"].extend(current_meta_dict["failure"])

    print(">>> retrieving relevant data...")
    # retrieve whole data
    load = data_dict["load_collector"]  # list (collector)
    speed = data_dict["speed_collector"]  # list (collector)

    # create a matching descriptive DataFrame
    metadata = pd.DataFrame.from_dict(data=meta_dict, orient="columns")
    return load, speed, metadata


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    machine_name = "PerschmannHermleC32USpindle"

    load, speed, metadata = main(project_dir, machine_name)

    # save relevant processes with corresponding metadata
    interim_dir_path = utils.get_interim_dir_path(project_dir)
    print(">>> saving compressed array using savez_compressed...")
    np.savez_compressed(os.path.join(interim_dir_path, "data"), load=load, speed=speed)
    print(">>> saving metadata at {}...".format(interim_dir_path))
    metadata.to_pickle(os.path.join(interim_dir_path, "metadata"))
    print("finished")

    # print(">>> saving load_collector at {}".format(interim_dir_path))
    # np.save(os.path.join(interim_dir_path, "load"), load, allow_pickle=True)
    # print(">>> saving speed_collector at {}".format(interim_dir_path))
    # np.save(os.path.join(interim_dir_path, "speed"), speed, allow_pickle=True)


# project_dir = "/home/adnene33/Documents/FM/Perschmann_Tool_Wear"
