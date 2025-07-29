'''Extracts moon phase and planetary body information from Astronomy API'''
import os
import base64
import json

import requests
from dotenv import load_dotenv

# Folder path for the json output
DATA_FILE_PATH = 'data'

# Authentication method for Astronomy API
USER_PASS = f"{os.environ.get('applicationId')}:{os.environ.get('applicationSecret')}"
AUTH_STRING = base64.b64encode(USER_PASS.encode()).decode()


HEADERS = {
    'Authorization': f'Basic {AUTH_STRING}',
    'Content-Type': 'application/json'
}

# Global variables
REGION_LATITUDE = +40.7128
REGION_LONGITUDE = -74.0060
DATE = '2025-07-28'
TIME = '00:00:00'


def get_planetary_positions(
    lat: float,
    lon: float,
    date: str,
    time: str,
    header: dict[str:str]
) -> None:
    '''Gets information on planetary bodies and saves it to a file as JSON'''

    # String concatenation method to ensure one line is broken into multiple for readability.
    # '+' is optional but included for clarity
    planetary_positions_url: str = (
        "https://api.astronomyapi.com/api/v2/bodies/positions"
        + f"?latitude={lat}"
        + f"&longitude={lon}"
        + "&elevation=0"
        + f"&from_date={date}"
        + f"&to_date={date}"
        + f"&time={time}"
    )

    response = requests.get(
        planetary_positions_url,
        headers=header,
        timeout=20
    )

    if response.status_code == 200:
        # Creates a data folder and a new json file inside it with the result from API call
        os.makedirs(DATA_FILE_PATH, exist_ok=True)
        json_path = os.path.join(
            DATA_FILE_PATH,
            'planetary_data.json'
        )

        with open(json_path, 'w',  encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2)
    else:
        print(f'Error {response.status_code}, {response.json()}')


if __name__ == "__main__":
    load_dotenv()
    get_planetary_positions(
        REGION_LATITUDE,
        REGION_LONGITUDE,
        DATE,
        TIME,
        HEADERS
    )
