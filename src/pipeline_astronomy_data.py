"""Module to pull together the full ETL pipeline for the astronomy data"""
import datetime

import logging
from dotenv import load_dotenv

from src.extract_astronomy_data import get_db_connection, get_planetary_positions, get_date_range
from src.transform_astronomy_data import filter_data
from src.load_astronomy_data import main
from src.astronomy_utils import make_request_headers


logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def run_pipeline():
    """Runs the astronomy pipeline from start to finish"""
    logging.info("Starting pipeline")

    # extract
    logging.info("Starting extract")
    extract_start = datetime.datetime.now()

    connection = get_db_connection()

    data = get_planetary_positions(
        {  # coordinates dict
            "lat": +51.30,
            "lon": -00.05
        },
        get_date_range(connection),
        make_request_headers()
    )
    extract_end = datetime.datetime.now()
    logging.info("Extract done in %s", extract_end-extract_start)

    # transform
    logging.info("Starting transform")
    transform_start = datetime.datetime.now()

    if not isinstance(data, dict):
        raise TypeError(f"Expected to receive a dict, got {type(data)}")
    if len(data) > 0:
        transformed_data = filter_data(data)
    else:
        raise ValueError(
            f"Data dict (type {type(data)}) appears to be empty: {data}")

    transform_end = datetime.datetime.now()
    logging.info("Transform done in %s", transform_end-transform_start)

    # load
    logging.info("Starting load")
    load_start = datetime.datetime.now()

    main(transformed_data)

    load_end = datetime.datetime.now()
    logging.info("Load done in %s", load_end-load_start)

    logging.info("Pipeline finished in %s", load_end-extract_start)


def handler(event, context):
    """handler function for lambda function"""
    try:
        run_pipeline()
        logging.info("%s : Lambda time remaining in MS:", event,
                     context.get_remaining_time_in_millis())
        return {"statusCode": 200}
    except (TypeError, ValueError, IndexError) as e:
        return {"statusCode": 500, "error": str(e)}


if __name__ == "__main__":
    load_dotenv()
    run_pipeline()
