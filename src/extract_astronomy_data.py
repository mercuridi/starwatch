'''Extracts moon phase and planetary body information from Astronomy API'''
import os
import base64
import json
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()
# ^ This needs removing from the global namespace before containerisation!!!
# If you leave this in stuff will start breaking later on - remove ASAP tbh
# Right now it has to be here because some assignments lower down *need* the
# .env to be loaded in order to work at all, and if the assignments break nothing happens

# Folder path for the json output
DATA_FILEPATH = '../data/'

# Authentication method for Astronomy API
USER_PASS = f"{os.environ.get('applicationId')}:{os.environ.get('applicationSecret')}"
AUTH_STRING = base64.b64encode(USER_PASS.encode()).decode()

# Set up headers for API request
HEADERS = {
    'Authorization': f'Basic {AUTH_STRING}',
    'Content-Type': 'application/json'
}


# Global variables
REGION_LATITUDE = +40.7128
REGION_LONGITUDE = -74.0060
COORDINATES = {
    "lat": REGION_LATITUDE,
    "lon": REGION_LONGITUDE
}
DATE_TODAY = datetime.now().date()
DATE_WEEK_FROM_NOW = DATE_TODAY + timedelta(days=6)
TIME = datetime.now().time().strftime("%H:%M:%S")


def get_planetary_positions(
    coordinates: dict[str:float],
    start_date: str,
    end_date: str,
    time: str,
    header: dict[str:str],
    data_filepath: str
) -> None:
    '''
    Gets information on planetary bodies from current day
    to next 7 days and saves it to a file as JSON
    '''

    # String concatenation method to ensure one line
    # is broken into multiple for readability.
    # '+' is optional but included for clarity
    planetary_positions_url = get_positions_url(coordinates, start_date, end_date, time)

    response = requests.get(
        planetary_positions_url,
        headers=header,
        timeout=20
    )

    return handle_response(response, data_filepath)


def handle_response(response: requests.Response, data_filepath: str) -> None:
    """Handles the API response; prints errors on fail and dumps to JSON on success"""
    if response.status_code == 200:
        json_path = make_dump_path(data_filepath)
        dump_json_data(response, json_path)
        return True
    else:
        print(f'Error {response.status_code}, {response.json()}')
        return False


def dump_json_data(response: requests.Response, json_path: str) -> None:
    """Dumps data in a context manager to ensure proper closing"""
    if not isinstance(response, requests.Response):
        raise TypeError(f"Expected to serialise a Response object, got {type(response)}")
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
        start_date: str,
        end_date: str,
        time: str
    ) -> str:
    """Constructs the API endpoint for the planetary positions data"""
    planetary_positions_url: str = (
        "https://api.astronomyapi.com/api/v2/bodies/positions"
        + f"?latitude={coordinates["lat"]}"
        + f"&longitude={coordinates["lon"]}"
        + "&elevation=0"
        + f"&from_date={start_date}"
        + f"&to_date={end_date}"
        + f"&time={time}"
    )
    return planetary_positions_url


if __name__ == "__main__":
    get_planetary_positions(
        COORDINATES,
        str(DATE_TODAY),
        str(DATE_WEEK_FROM_NOW),
        str(TIME),
        HEADERS,
        DATA_FILEPATH
    )
