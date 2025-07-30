# pylint: skip-file
import os
import base64
from datetime import datetime, timedelta

import requests
import pytest
from unittest.mock import MagicMock, Mock

from src.extract_astronomy_data import dump_json_data, make_dump_path, get_positions_url, get_planetary_positions

@pytest.fixture
def data():
    return {
        # Folder path for the json output
        "data_filepath": '../data/',

        # Set up headers for API request
        "headers": {
            'Authorization': f'Basic {base64.b64encode(f"{os.environ.get('applicationId')}:{os.environ.get('applicationSecret')}".encode()).decode()}',
            'Content-Type': 'application/json'
        },

        "coordinates": {
            "lat": +40.7128,
            "lon": -74.0060
        },
        "dates": {
            "start": datetime.strptime("2025-07-29", "%Y-%m-%d").date(),
            "end": datetime.strptime("2025-07-29", "%Y-%m-%d").date() + timedelta(days=6),
        },
        "time": datetime.strptime("00:00:00", "%H:%M:%S").time()
    }

def test_make_dump_path(mocker, data):
    mock_os = mocker.patch(__name__ + ".os.makedirs", return_value=None)
    assert make_dump_path(data["data_filepath"]) == "../data/planetary_data.json"
    assert mock_os.call_count == 1

def test_get_positions_url(data):
    assert get_positions_url(
        data["coordinates"],
        data["dates"],
        data["time"]
    ) == "https://api.astronomyapi.com/api/v2/bodies/positions?latitude=40.7128&longitude=-74.006&elevation=0&from_date=2025-07-29&to_date=2025-08-04&time=00:00:00"

def test_get_planetary_positions_api_ok(mocker, data):
    api_mock_true = MagicMock()
    api_mock_true.status_code = 200
    mock_dump = mocker.patch("src.extract_astronomy_data.dump_json_data", return_value=None)
    mock_os = mocker.patch(__name__ + ".os.makedirs", return_value=None)
    mocker.patch(__name__ + ".requests.get", return_value=api_mock_true)
    assert get_planetary_positions(
        data["coordinates"],
        data["dates"],
        data["time"],
        data["headers"],
        data["data_filepath"]
    ) == True
    assert mock_dump.call_count == 1
    assert mock_os.call_count == 1


def test_get_planetary_positions_api_down(mocker, data):
    api_mock_false = MagicMock()
    api_mock_false.status_code = 400
    mock_os = mocker.patch(__name__ + ".os.makedirs", return_value=None)
    mock_api = mocker.patch(__name__ + ".requests.get", return_value=api_mock_false)
    assert get_planetary_positions(
        data["coordinates"],
        data["dates"],
        data["time"],
        data["headers"],
        data["data_filepath"]
    ) == False
    assert mock_os.call_count == 0
    assert mock_api.call_count == 1


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