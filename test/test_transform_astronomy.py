# pylint: skip-file
import json

import pytest
from unittest.mock import MagicMock, Mock, patch

from src.transform_astronomy_data import filter_data, add_record

@pytest.fixture
def raw_data():
    with open("data/astronomy_test_data.json") as f:
        return json.load(f)

def test_filter_data(raw_data):
    filtered_data = filter_data(raw_data)
    assert set(list(filtered_data.columns)) == set(
        [
            'date', 'latitude', 'longitude', 
            'planetary_body', 'constellation', 
            'right_ascension_hours', 'right_ascension_string', 
            'declination_degrees', 'declination_string', 
            'astronomical_units', 
            'altitude_degrees', 'altitude_string', 
            'azimuth_degrees', 'azimuth_string'
        ]
    )

def test_add_record(raw_data):
    longitude = raw_data['data']['observer']['location']['longitude']
    latitude = raw_data['data']['observer']['location']['latitude']
    data_of_planetary_bodies = raw_data['data']['table']['rows']
    body = data_of_planetary_bodies[0]
    name = body['entry']['name']
    records = []

    add_record(longitude, latitude, records, name, body['cells'][0])

    assert len(records) == 1

    added_record = records[0]
    assert added_record["date"] == '2025-08-10'
    assert added_record["latitude"] == 51.3
    assert added_record["longitude"] == -0.05
    assert added_record["planetary_body"] == "Sun"
    assert added_record["constellation"] == "Cancer"
    assert added_record["right_ascension_hours"] == "9.35"
    assert added_record["right_ascension_string"] == "09h 21m 00s"
    assert added_record["declination_degrees"] == "15.51"
    assert added_record["declination_string"] == '15° 30\' 36"'
    assert added_record["astronomical_units"] == "1.01354"
    assert added_record["altitude_degrees"] == "54.09"
    assert added_record["altitude_string"] == '54° 5\' 24"'
    assert added_record["azimuth_degrees"] == "177.44"
    assert added_record["azimuth_string"] == '177° 26\' 24"'


