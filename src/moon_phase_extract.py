''' 
Generates a moon phase image using the Astronomy API based on a specific region
Returns the image
'''

# pylint:disable=import-error
import os
from datetime import datetime
import requests

import src.astronomy_utils


def get_moon_phase_image(
        latitude: str,
        longitude: str,
        date: str,
        headers: dict,
        url: str,
) -> None:
    '''
    Uses the Astronomy API to generate a moon phase image using given coordinates
    '''

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

    # Post request to get moon phase image
    try:
        response = requests.post(
            url,
            headers=headers,
            json=moon_phase_payload,
            timeout=60
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error, failed to fetch moon phase image URL: {e}")
        return

    # Convert & return image url from post request to jpg
    try:
        image_url = response.json()['data']['imageUrl']
        img_data = requests.get(image_url, timeout=30).content

        return img_data

    except Exception as e:
        print(f"Error, failed to download moon phase image: {e}")
