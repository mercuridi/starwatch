''' 
Generates a moon phase image using the Astronomy API based on a specific region
Saves this image to ../data
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
        save_path='data/moon_phase.jpg'
) -> None:
    '''
    Uses the Astronomy API to generate a moon phase image using given coordinates
    '''
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

    # Post request to get moon phase image
    try:
        response = requests.post(
            moon_phase_url,
            headers=headers,
            json=moon_phase_payload,
            timeout=300
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error Failed to fetch moon phase image URL: {e}")
        return

    # Convert & save image url from post request to jpg
    try:
        image_url = response.json()['data']['imageUrl']
        img_data = requests.get(image_url, timeout=300).content

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as f:
            f.write(img_data)

    except Exception as e:
        print(f"Error Failed to download or save moon phase image: {e}")


if __name__ == "__main__":

    TEST_LATITUDE = 51.30
    TEST_LONGITUDE = -0.05
    TEST_DATE = datetime.now().date()

    # Test image
    get_moon_phase_image(
        TEST_LATITUDE,
        TEST_LONGITUDE,
        TEST_DATE,
        src.astronomy_utils.make_request_headers()
    )
