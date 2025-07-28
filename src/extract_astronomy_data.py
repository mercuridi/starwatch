import os
import base64
import requests
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

moon_phase_payload = {
    "observer": {
        "latitude": region_latitude,
        "longitude": region_longitude,
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

moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"


def get_moon_phase_image():

    response = requests.post(
        moon_phase_url, headers=headers, json=moon_phase_payload)
    if response.status_code == 200:
        print(response.json()['data']['imageUrl'])
    else:
        print(f'Error {response.status_code}')


if __name__ == "__main__":
    get_moon_phase_image()
