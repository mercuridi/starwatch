import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv('src/.env')


user_pass = f"{os.environ.get('applicationId')}:{os.environ.get("applicationSecret")}"
auth_string = base64.b64encode(user_pass.encode()).decode()
headers = {
    'Authorization': f'Basic {auth_string}',
    'Content-Type': 'application/json'

}

region_latitude = 40.7128
region_longitude = -74.0060
date = '2025-07-28'


moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"


def get_planetary_positions(latitude, longitude, date, time):

    planetary_positions_url = f'https://api.astronomyapi.com/api/v2/bodies/positions?latitude={latitude}&longitude={longitude}&elevation=0&from_date={date}&to_date={date}&time={time}'

    response = requests.get(planetary_positions_url, headers=headers)

    if response.status_code == 200:
        directory = "src/extracted_data"
        os.makedirs(directory, exist_ok=True)

        with open('src/extracted_data/planetary_positions.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
    else:
        print(f'Error {response.status_code}, {response.json()}')


def get_moon_phase_image(latitude, longitude, date):

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
        moon_phase_url, headers=headers, json=moon_phase_payload)
    if response.status_code == 200:
        image_url = response.json()['data']['imageUrl']
        img_data = requests.get(image_url).content

        with open('src/extracted_data/moon_phase.jpg', 'wb') as f:
            f.write(img_data)

    else:
        print(f'Error {response.status_code}')


if __name__ == "__main__":
    get_planetary_positions(
        region_latitude, region_longitude, date, '00:00:00')
    get_moon_phase_image(region_latitude, region_longitude, date)
