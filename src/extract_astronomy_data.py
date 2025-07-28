'''Extracts moon phase and planetary body information from Astronomy API'''
import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv('src/.env')


user_pass = f"{os.environ.get('applicationId')}:{os.environ.get("applicationSecret")}"
auth_string = base64.b64encode(user_pass.encode()).decode()
headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/json'
}

REGION_LATITUDE = 40.7128
REGION_LONGITIDE = -74.0060
DATE = '2025-07-28'


def get_planetary_positions(latitude, longitude, date, time, header):
    '''Gets information on planetary bodies and saves it to a file as JSON'''
    planetary_positions_url = f'https://api.astronomyapi.com/api/v2/bodies/positions?latitude={latitude}&longitude={longitude}&elevation=0&from_date={date}&to_date={date}&time={time}'

    response = requests.get(planetary_positions_url, headers=header)

    if response.status_code == 200:
        directory = "src/extracted_data"
        os.makedirs(directory, exist_ok=True)

        with open('src/extracted_data/planetary_positions.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
    else:
        print(f'Error {response.status_code}, {response.json()}')


def get_moon_phase_image(latitude, longitude, date, header):
    '''Generates a moon phase image based on latitude and longitude and saves as png'''
    moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"

    moon_phase_payload = {
        "observer": {
            "latitude": latitude,
            "longitude": longitude,
            "date": date
        },
        "view": {
            "type": "landscape-simple",
            "orientation": "north-up"
        },
        "style": {
            "moonStyle": "default",
            "backgroundStyle": "solid",
            "backgroundColor": "black",
            "headingColor": "white",
            "textColor": "white"
        }
    }
    response = requests.post(
        moon_phase_url, headers=header, json=moon_phase_payload)
    if response.status_code == 200:
        image_url = response.json()['data']['imageUrl']
        img_data = requests.get(image_url).content

        with open('src/extracted_data/moon_phase.jpg', 'wb') as f:
            f.write(img_data)

    else:
        print(f'Error {response.status_code}')


if __name__ == "__main__":
    get_planetary_positions(
        REGION_LATITUDE, REGION_LONGITIDE, DATE, '00:00:00', headers)
    get_moon_phase_image(REGION_LATITUDE, REGION_LONGITIDE, DATE, headers)
