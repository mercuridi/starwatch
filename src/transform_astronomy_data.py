'''Gets JSON data from specified file, filters for relevant columns and converts into dataframe'''

import json
import logging
import pandas as pd

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

FILE_PATH = "../data/planetary_data.json"


def get_json_data(file_path: str) -> dict:
    '''Gets JSON from file and returns'''
    try:

        with open(file_path, 'r', encoding='utf-8') as file:
            logging.info('JSON Data Retrieved')
            return json.load(file)
    except FileNotFoundError:
        logging.info('Error, No file found')
        return {}


def filter_data(json_data: dict) -> pd.DataFrame:
    '''
    Takes in JSON and filters for required data as key value pairs in a list of dictionaries
    Converts dictionary into a dataframe and returns
    '''
    longitude = json_data['data']['observer']['location']['longitude']
    latitude = json_data['data']['observer']['location']['latitude']
    data_of_planetary_bodies = json_data['data']['table']['rows']

    records = []

    # Loops for each planet/star
    for planetary_body in data_of_planetary_bodies:
        name = planetary_body['entry']['name']

        # Loops for each date
        for record in planetary_body['cells']:
            # Creates list of dictionaries of all relevant data from JSON
            add_record(longitude, latitude, records, name, record)

    logging.info('JSON Data Filtered')
    return pd.DataFrame(records)


def add_record(longitude, latitude, records, name, record):
    """Wrapper around append line for modularisation of script"""
    records.append({
        # Gets date in YYYY-MM-DD
        "date":
            record['date'].split("T")[0],
        "latitude":
            latitude,
        "longitude":
            longitude,
        "planetary_body":
            name,
        "constellation":
            record['position']['constellation']['name'],
        "right_ascension_hours":
            record['position']['equatorial']['rightAscension']['hours'],
        "right_ascension_string":
            record['position']['equatorial']['rightAscension']['string'],
        "declination_degrees":
            record['position']['equatorial']['declination']['degrees'],
        "declination_string":
            record['position']['equatorial']['declination']['string'],
        "astronomical_units":
            record['distance']['fromEarth']['au'],
        "altitude_degrees":
            record['position']['horizontal']['altitude']['degrees'],
        "altitude_string":
            record['position']['horizontal']['altitude']['string'],
        "azimuth_degrees":
            record['position']['horizontal']['azimuth']['degrees'],
        "azimuth_string":
            record['position']['horizontal']['azimuth']['string']
    })


if __name__ == "__main__":
    data = get_json_data(FILE_PATH)

    if not isinstance(data, dict):
        raise TypeError(f"Expected to receive a dict, got {type(data)}")
    if len(data) > 0:
        transformed_data = filter_data(data)
