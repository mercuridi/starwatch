'''Gets JSON data from specified file, filters for relevant columns and converts into dataframe'''

# pylint:disable=line-too-long

import json
import pandas as pd

FILE_PATH = "data/planetary_data.json"


def get_json_data(file_path: str) -> dict:
    '''Gets JSON from file and returns'''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return 'Error, No file found'


def filter_data(json_data: dict) -> pd.DataFrame:
    '''
    Takes in JSON and filters for required data as key value pairs in a dictionary
    Converts dictionary into a dataframe and returns
    '''
    longitude = json_data['data']['observer']['location']['longitude']
    latitude = json_data['data']['observer']['location']['latitude']
    data_of_planetary_bodies = json_data['data']['table']['rows']

    records = []
    for planetary_body in data_of_planetary_bodies:
        name = planetary_body['entry']['name']

        for record in planetary_body['cells']:
            # Creates dict of all relevant data from JSON
            records.append({
                # Gets date in YYYY-MM-DD
                "date": record['date'].split("T")[0],
                "latitude": latitude,
                "longitude": longitude,
                "planetary_body": name,
                "constellation": record['position']['constellation']['name'],
                "right_ascension_hours": record['position']['equatorial']['rightAscension']['hours'],
                "right_ascension_string": record['position']['equatorial']['rightAscension']['string'],
                "declination_degrees": record['position']['equatorial']['declination']['degrees'],
                "declination_string": record['position']['equatorial']['declination']['string'],
                "distance_km": record['distance']['fromEarth']['km'],
                "altitude_degrees": record['position']['horizontal']['altitude']['degrees'],
                "altitude_string": record['position']['horizontal']['altitude']['string'],
                "azimuth_degrees": record['position']['horizontal']['azimuth']['degrees'],
                "azimuth_string": record['position']['horizontal']['azimuth']['string']
            })

    return pd.DataFrame(records)


if __name__ == "__main__":
    data = get_json_data(FILE_PATH)
    if data:
        transformed_data = filter_data(data)
