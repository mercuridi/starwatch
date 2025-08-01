"""Module to pull together the full ETL pipeline for the astronomy data"""
import datetime

from dotenv import load_dotenv

from extract_astronomy_data import get_db_connection, get_planetary_positions, get_date_range
from transform_astronomy_data import filter_data
from load_astronomy_data import main
from astronomy_utils import make_request_headers

def run_pipeline():
    """Runs the astronomy pipeline from start to finish"""
    print("Starting pipeline")

    # extract
    print("Starting extract")
    extract_start = datetime.datetime.now()

    connection = get_db_connection()

    data = get_planetary_positions(
        { # coordinates dict
            "lat": +51.30,
            "lon": -00.05
        },
        get_date_range(connection),
        make_request_headers()
    )
    extract_end = datetime.datetime.now()
    print(f"Extract done in {extract_end-extract_start}")


    # transform
    print("Starting transform")
    transform_start = datetime.datetime.now()

    if not isinstance(data, dict):
        raise TypeError(f"Expected to receive a dict, got {type(data)}")
    if len(data) > 0:
        transformed_data = filter_data(data)
    else:
        raise ValueError(f"Data dict (type {type(data)}) appears to be empty: {data}")

    transform_end = datetime.datetime.now()
    print(f"Transform done in {transform_end-transform_start}")

    # load
    print("Starting load")
    load_start = datetime.datetime.now()

    main(transformed_data)

    load_end = datetime.datetime.now()
    print(f"Load done in {load_end-load_start}")

    print(f"Pipeline finished in {load_end-extract_start}")


def handler(event, context):
    """handler function for lambda function"""
    try:
        run_pipeline()
        print(f"{event} : Lambda time remaining in MS:",
              context.get_remaining_time_in_millis())
        return {"statusCode": 200}
    except (TypeError, ValueError, IndexError) as e:
        return {"statusCode": 500, "error": str(e)}


if __name__ == "__main__":
    load_dotenv()
    run_pipeline()
