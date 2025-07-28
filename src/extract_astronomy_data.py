'''Extracts moon phase and planetary body information from Astronomy API'''
import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv('src/.env')

# Authentication method for Astronomy API
user_pass = f"{os.environ.get('applicationId')}:{os.environ.get("applicationSecret")}"
auth_string = base64.b64encode(user_pass.encode()).decode()


headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/json'
}

# Global variables
REGION_LATITUDE = 40.7128
REGION_LONGITUDE = -74.0060
DATE = '2025-07-28'
TIME = '00:00:00'


def get_planetary_positions(lat, lon, date, time, header):
    '''Gets information on planetary bodies and saves it to a file as JSON'''
    planetary_positions_url = (
        "https://api.astronomyapi.com/api/v2/bodies/positions"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&elevation=0"
        f"&from_date={date}"
        f"&to_date={date}"
        f"&time={time}"
    )

    response = requests.get(planetary_positions_url,
                            headers=header, timeout=20)

    if response.status_code == 200:

        with open('src/planetary_positions.json', 'w',  encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2)
    else:
        print(f'Error {response.status_code}, {response.json()}')


if __name__ == "__main__":
    get_planetary_positions(
        REGION_LATITUDE, REGION_LONGITUDE, DATE, TIME, headers)
