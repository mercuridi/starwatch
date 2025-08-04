'''Extracts moon phase and planetary body information from Astronomy API'''
import os
import json
from datetime import datetime, timedelta

import psycopg2
import requests
from dotenv import load_dotenv

import src.astronomy_utils

def get_db_connection() -> psycopg2.extensions.connection:
    """
    Returns a connection to the starwatch RDS database
    Assumes a .env has been loaded with the appropriate keys
    """
    try:
        conn_string = f"""
        host='{os.environ.get("DB_HOST")}'
        dbname='{os.environ["DB_NAME"]}'
        user='{os.environ["DB_USER"]}'
        password='{os.environ["DB_PASSWORD"]}'
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
    time: str=str(datetime.now().time().strftime("%H:%M:%S"))
) -> dict:
    '''
    Gets information on planetary bodies from current day
    to next 7 days and saves it to a file as JSON
    '''

    planetary_positions_url = get_positions_url(coordinates, dates, time)

    response = requests.get(
        planetary_positions_url,
        headers=header,
        timeout=20
    )

    if not isinstance(response, requests.Response):
        raise TypeError(
            f"Expected a Response object, got {type(response)}")

    if response.status_code == 200:
        return response.json()

    raise RuntimeError(f"Error {response.status_code}, {response.json()}")


def get_positions_url(
    coordinates: dict[str:float],
    dates: dict[str:datetime.date],
    time: str
) -> str:
    """Constructs the API endpoint for the planetary positions data"""
    # String concatenation method to ensure one line
    # is broken into multiple for readability.
    # '+' is optional but included for clarity
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
    load_dotenv()
    connection = get_db_connection()

    data = get_planetary_positions(
        { # coordinates dict
            "lat": +51.30,
            "lon": -00.05
        },
        get_date_range(connection),
        src.astronomy_utils.make_request_headers()
    )

    with open('astronomy_test_data.json', 'w', encoding="utf8") as f:
        json.dump(data, f, indent=2)
