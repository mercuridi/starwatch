# pylint: skip-file
import os
import base64
from datetime import datetime, timedelta

import requests
import pytest
from unittest.mock import MagicMock, Mock, patch
import pandas as pd

from src.extract_astronomy_data import get_positions_url, get_planetary_positions, get_date_range


@pytest.fixture
def mock_conn_with_data():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [1]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


@pytest.fixture
def mock_conn_empty():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [0]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


@patch('src.extract_astronomy_data.datetime')
def test_get_date_range_with_data(mock_datetime, mock_conn_with_data):
    fake_today = datetime(2024, 1, 1)
    mock_datetime.now.return_value = fake_today

    date_range = get_date_range(mock_conn_with_data)

    expected_start = fake_today.date() + timedelta(days=6)
    expected_end = expected_start + timedelta(days=1)

    assert date_range == {
        "start": expected_start,
        "end": expected_end
    }


@patch('src.extract_astronomy_data.datetime')
def test_get_date_range_empty(mock_datetime, mock_conn_empty):
    fake_today = datetime(2024, 1, 1)
    mock_datetime.now.return_value = fake_today

    date_range = get_date_range(mock_conn_empty)

    expected_start = fake_today.date()
    expected_end = expected_start + timedelta(days=6)

    assert date_range == {
        "start": expected_start,
        "end": expected_end
    }


@pytest.fixture
def data():
    return {
        # Folder path for the json output
        "data_filepath": '../data/',

        # Set up headers for API request

        "headers": {
            'Authorization': f'Basic' + str(base64.b64encode(f"{os.environ.get('applicationId')}:{os.environ.get('applicationSecret')}".encode()).decode()),
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


def test_get_positions_url(data):
    assert get_positions_url(
        data["coordinates"],
        data["dates"],
        data["time"]
    ) == "https://api.astronomyapi.com/api/v2/bodies/positions?latitude=40.7128&longitude=-74.006&elevation=0&from_date=2025-07-29&to_date=2025-08-04&time=00:00:00"


def test_get_planetary_positions_api_ok(mocker, data):
    api_mock_true = MagicMock(spec=requests.Response)
    api_mock_true.status_code = 200
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=api_mock_true)
    get_planetary_positions(
        data["coordinates"],
        data["dates"],
        data["time"]
    )
    assert mock_api.call_count == 1

def test_get_planetary_positions_api_down(mocker, data):
    api_mock_false = MagicMock(spec=requests.Response)
    api_mock_false.status_code = 400
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=api_mock_false)
    with pytest.raises(RuntimeError):
        get_planetary_positions(
            data["coordinates"],
            data["dates"],
            data["time"]
        )
        assert mock_api.call_count == 1
