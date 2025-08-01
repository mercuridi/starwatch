'''Extracts moon phase and planetary body information from Astronomy API'''
import os
import json
from datetime import datetime, timedelta

import psycopg2
import requests

from astronomy_utils import make_request_headers

# Folder path for the json output
DATA_FILEPATH = '../data/'

COORDINATES = {
    "lat": +40.7128,
    "lon": -74.0060
}

def get_db_connection() -> psycopg2.extensions.connection:
    """Returns a connection to the starwatch RDS database"""
    try:
        conn_string = f"""
        host='{os.environ.get("db_host")}'
        dbname='{os.environ["db_name"]}'
        user='{os.environ["db_username"]}'
        password='{os.environ["db_password"]}'
        """
        return psycopg2.connect(conn_string)

    except psycopg2.OperationalError as e:
        raise RuntimeError(f"Database connection failed: {e}") from e


def check_data_in_tables(conn: psycopg2.extensions.connection) -> bool:
    """Checks if the forecast and distance tables in the database have any data.
    Returns True if tables have data - false if tables are empty"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM forecast;
    """)
    forecast_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) 
        FROM distance;
    """)
    distance_count = cursor.fetchone()[0]
    return forecast_count > 0 and distance_count > 0


def get_date_range(conn) -> dict[str, datetime.date]:
    """Determines the date period for which data is downloaded. 
    7 days worth of data if the db is empty;
    Otherwise, 1 day of data starting 7 days in advance.
    """
    today = datetime.now().date()
    date_week_from_now = today + timedelta(days=6)

    if check_data_in_tables(conn):
        return {
            "start": date_week_from_now,
            "end": date_week_from_now + timedelta(days=1)
        }
    return {
        "start": today,
        "end": date_week_from_now
    }


def get_planetary_positions(
    coordinates: dict[str:float],
    dates: dict[str:datetime.date],
    header: dict[str:str],
    data_filepath: str,
    time: str=str(datetime.now().time().strftime("%H:%M:%S"))
) -> bool:
    '''
    Gets information on planetary bodies from current day
    to next 7 days and saves it to a file as JSON
    '''

    # String concatenation method to ensure one line
    # is broken into multiple for readability.
    # '+' is optional but included for clarity
    planetary_positions_url = get_positions_url(coordinates, dates, time)

    response = requests.get(
        planetary_positions_url,
        headers=header,
        timeout=20
    )

    return handle_response(response, data_filepath)


def handle_response(response: requests.Response, data_filepath: str) -> bool:
    """Handles the API response; prints errors on fail and dumps to JSON on success"""
    if response.status_code == 200:
        json_path = make_dump_path(data_filepath)
        dump_json_data(response, json_path)
        return True

    print(f'Error {response.status_code}, {response.json()}')
    return False


def dump_json_data(response: requests.Response, json_path: str) -> None:
    """Dumps data in a context manager to ensure proper closing"""
    if not isinstance(response, requests.Response):
        raise TypeError(
            f"Expected to serialise a Response object, got {type(response)}")
    if not isinstance(json_path, str):
        raise TypeError("Passed json_path must be a string")
    if len(json_path) == 0:
        raise ValueError("Given empty string for json_path")
    with open(json_path, 'w',  encoding='utf-8') as f:
        json.dump(response.json(), f, indent=2)


def make_dump_path(data_filepath: str) -> str:
    """Ensures the data directory exists and returns a path to it"""
    os.makedirs(data_filepath, exist_ok=True)
    json_path = os.path.join(
        data_filepath,
        'planetary_data.json'
    )
    return json_path


def get_positions_url(
    coordinates: dict[str:float],
    dates: dict[str:datetime.date],
    time: str
) -> str:
    """Constructs the API endpoint for the planetary positions data"""
    planetary_positions_url: str = (
        "https://api.astronomyapi.com/api/v2/bodies/positions"
        + f"?latitude={coordinates['lat']}"
        + f"&longitude={coordinates['lon']}"
        + "&elevation=0"
        + f"&from_date={dates['start']}"
        + f"&to_date={dates['end']}"
        + f"&time={time}"
    )
    return planetary_positions_url


if __name__ == "__main__":
    connection = get_db_connection()
    DATES = get_date_range(connection)

    get_planetary_positions(
        COORDINATES,
        DATES,
        make_request_headers(),
        DATA_FILEPATH
    )
