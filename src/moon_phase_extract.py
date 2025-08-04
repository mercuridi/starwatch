import requests
import os
from datetime import datetime

import src.astronomy_utils


def get_moon_phase_image(latitude, longitude, date, headers, save_path='data/moon_phase.jpg'):

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

    try:
        response = requests.post(
            moon_phase_url, headers=headers, json=moon_phase_payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Error] Failed to fetch moon phase image URL: {e}")
        return

    try:
        image_url = response.json()['data']['imageUrl']
        img_data = requests.get(image_url).content

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as f:
            f.write(img_data)

    except Exception as e:
        print(f"[Error] Failed to download or save moon phase image: {e}")
