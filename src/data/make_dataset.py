# -*- coding: utf-8 -*-
import click
import logging
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import utils
import prepare_data
import prepare_labels
import process_dataset


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    machine_name = "PerschmannHermleC32USpindle"
    raw_dir_path = utils.get_raw_dir_path(project_dir)
    interim_dir_path = utils.get_interim_dir_path(project_dir)
    processed_dir_path = utils.get_processed_dir_path(project_dir)

    # load relevant data collectors after selection
    collector_load, collector_speed, metadata = prepare_data.main(
        project_dir, machine_name
    )
    X_load = utils.to_same_length_time_series_dataset(collector_load)
    X_speed = utils.to_same_length_time_series_dataset(collector_speed)

    # get labels
    labels = prepare_labels.create_labels_from_metadata(metadata)
    """TO DO: transform labels into categories, then one hot encode"""
    
    # compute autocorrelation
    X_load_autocorr = process_dataset.to_autocorrelation_dataset(X_load)
    X_speed_autocorr = process_dataset.to_autocorrelation_dataset(X_speed)
    
    # 

    print("LENGTH LABEL VECTOR {}".format(len(labels)))
    print("project_dir: {}".format(project_dir))
    print("FINISHED")

    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # galactic

    main()
