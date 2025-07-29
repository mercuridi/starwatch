# pylint: skip-file
import os
import base64
from datetime import datetime, timedelta

import requests
import pytest
from unittest.mock import MagicMock, Mock

from src.extract_astronomy_data import dump_json_data, make_dump_path, get_positions_url, get_planetary_positions

# Global constants used for testing

# Folder path for the json output
DATA_FILEPATH = '../data/'

# Authentication method for Astronomy API
USER_PASS = f"{os.environ.get('applicationId')}:{os.environ.get('applicationSecret')}"
AUTH_STRING = base64.b64encode(USER_PASS.encode()).decode()

# Set up headers for API request
HEADERS = {
    'Authorization': f'Basic {AUTH_STRING}',
    'Content-Type': 'application/json'
}

# Global constants
# Latitude and longitude are placeholders
REGION_LATITUDE = +40.7128
REGION_LONGITUDE = -74.0060
COORDINATES = {
    "lat": REGION_LATITUDE,
    "lon": REGION_LONGITUDE
}
DATE_TODAY = datetime.strptime("2025-07-29", "%Y-%m-%d").date()
DATE_WEEK_FROM_NOW = DATE_TODAY + timedelta(days=6)
TIME = datetime.strptime("00:00:00", "%H:%M:%S").time()

def test_make_dump_path(mocker):
    mocker.patch(__name__ + ".os.makedirs", return_value=None)
    assert make_dump_path(DATA_FILEPATH) == "../data/planetary_data.json"

def test_get_positions_url():
    assert get_positions_url(
        COORDINATES,
        str(DATE_TODAY),
        str(DATE_WEEK_FROM_NOW),
        TIME
    ) == "https://api.astronomyapi.com/api/v2/bodies/positions?latitude=40.7128&longitude=-74.006&elevation=0&from_date=2025-07-29&to_date=2025-08-04&time=00:00:00"

def test_get_planetary_positions_api_ok(mocker):
    mocker.patch("src.extract_astronomy_data.dump_json_data", return_value=None)
    mocker.patch(__name__ + ".os.makedirs", return_value=None)
    api_mock_true = MagicMock()
    api_mock_true.status_code = 200
    mocker.patch(__name__ + ".requests.get", return_value=api_mock_true)
    assert get_planetary_positions(
        COORDINATES,
        str(DATE_TODAY),
        str(DATE_WEEK_FROM_NOW),
        TIME,
        HEADERS,
        DATA_FILEPATH
    ) == True

def test_get_planetary_positions_api_down(mocker):
    mocker.patch(__name__ + ".os.makedirs", return_value=None)
    api_mock_false = MagicMock()
    api_mock_false.status_code = 400
    mocker.patch(__name__ + ".requests.get", return_value=api_mock_false)
    assert get_planetary_positions(
        COORDINATES,
        str(DATE_TODAY),
        str(DATE_WEEK_FROM_NOW),
        TIME,
        HEADERS,
        DATA_FILEPATH
    ) == False

def test_dump_json_data_bad_input():
    mock_response = Mock(spec=requests.Response)
    mock_path = "path"
    with pytest.raises(TypeError):
        dump_json_data("string", mock_path)
    with pytest.raises(TypeError):
        dump_json_data(10, mock_path)
    with pytest.raises(TypeError):
        dump_json_data(mock_response, set())
    with pytest.raises(TypeError):
        dump_json_data(mock_response, 10)
    with pytest.raises(ValueError):
        dump_json_data(mock_response, "")