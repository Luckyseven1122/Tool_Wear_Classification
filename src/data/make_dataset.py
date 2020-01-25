# -*- coding: utf-8 -*-
import click
import logging
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import prepare_data


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    machine_name = "PerschmannHermleC32USpindle"
    raw_dir_path = os.path.join(project_dir, "data", "raw")
    interim_dir_path = os.path.join(project_dir, "data", "interim")
    processes_dir_path = os.path.join(project_dir, "data", "processes")

    # load relevant data collectors after selection
    load_collector, speed_collector, metadata = prepare_data.main(
        project_dir, machine_name
    )
    print("load_collector.type = {}".format(type(load_collector)))
    print("load_collector.length = {}".format(len(load_collector)))

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
