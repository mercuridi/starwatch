"""Extracts the Astronomy Picture of the Day and Near-Earth Objects from the NASA API"""
import os
from datetime import date
import requests as reqs
from dotenv import load_dotenv

load_dotenv()
TODAY = str(date.today())
api_key = os.environ.get("api_key")

APOD_URL = "https://api.nasa.gov/planetary/apod"
apod_params = {
    "api_key": api_key,
    "date": TODAY
}

NEO_URL = "https://api.nasa.gov/neo/rest/v1/feed"
neo_params = {
    "start_date": TODAY,
    "end_date": TODAY,
    "api_key": api_key
}


def get_image_details(url: str, apod_query_params: dict[str, str]) -> tuple[str, str, str]:
    """Retrieves the image title, the image and the image explanation from the NASA API.

    Raises:
        RuntimeError: If the API request fails.
        ValueError: If today's APOD is not an image."""
    response = reqs.get(url, params=apod_query_params, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch APOD data: {response.status_code} - {response.text}")

    data = response.json()

    if data.get('media_type') != 'image':
        raise ValueError("Today's APOD is not an image.")

    title = data.get('title')
    explanation = data.get('explanation')
    image_url = data.get('hdurl') or data.get('url')

    return title, explanation, image_url


def get_neos(url: str, neo_query_params: dict[str, str]) -> list[dict[str, str]]:
    """Retrieves the information of the objects near Earth today

    Raises:
        RuntimeError: If the API request fails."""
    response = reqs.get(url, params=neo_query_params, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch NEO data: {response.status_code} - {response.text}")

    data = response.json()
    neos_today = data.get("near_earth_objects", {}).get(TODAY, [])

    neo_info = []
    for neo in neos_today:
        name = neo.get("name")[1:-1]
        diameter_min = round(neo.get("estimated_diameter", {}).get(
            "meters", {}).get("estimated_diameter_min"), 1)
        diameter_max = round(neo.get("estimated_diameter", {}).get(
            "meters", {}).get("estimated_diameter_max"), 1)
        hazardous = neo.get("is_potentially_hazardous_asteroid")
        approach_data = neo.get("close_approach_data", [{}])[0]
        miss_distance_km = round(float(approach_data.get(
            "miss_distance", {}).get("kilometers")), 1)
        relative_velocity_kmph = round(float(approach_data.get(
            "relative_velocity", {}).get("kilometers_per_hour")), 1)

        neo_info.append({
            "name": name,
            "diameter_min_m": diameter_min,
            "diameter_max_m": diameter_max,
            "hazardous": hazardous,
            "miss_distance_km": miss_distance_km,
            "relative_velocity_kmph": relative_velocity_kmph
        })

    return neo_info


if __name__ == "__main__":
    get_image_details(APOD_URL, apod_params)
    get_neos(NEO_URL, neo_params)
