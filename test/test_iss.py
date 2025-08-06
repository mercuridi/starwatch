# pylint: skip-file

from unittest.mock import MagicMock
from datetime import datetime

import requests
import pytest
import freezegun

from src.iss_etl import get_iss_lat_long_now, get_passes, present_iss_passes

LONDON_LAT = +51.30
LONDON_LON = -00.05
STATIC_TIMESTAMP=1754469547
STATIC_DATETIME=datetime.fromtimestamp(STATIC_TIMESTAMP)

@pytest.fixture
def tle_fix():
    return """ISS (ZARYA)
1 25544U 98067A   25217.57738833  .00008075  00000-0  14750-3 0  9991
2 25544  51.6349  62.2717 0001595 155.7040 204.4024 15.50349286522825"""

def test_lat_long_ok(mocker):
    loc_dict = {"iss_position": {"latitude": LONDON_LAT, "longitude": LONDON_LON}}
    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.json = MagicMock(return_value=loc_dict)
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=req_mock)
    lat, lon = get_iss_lat_long_now()
    assert mock_api.call_count == 1
    assert lat == +51.30
    assert lon == -00.05

def test_lat_long_fail(mocker):
    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 400
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=req_mock)
    with pytest.raises(RuntimeError):
        _, _ = get_iss_lat_long_now()
    assert mock_api.call_count == 1

@freezegun.freeze_time(STATIC_DATETIME)
def test_get_passes(mocker, tle_fix):
    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.text = tle_fix
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=req_mock)

    assert get_passes(LONDON_LAT, LONDON_LON) == {'request': {'datetime': 1754473147, 'latitude': -0.05, 'longitude': 51.3, 'altitude': 0, 'passes': 1}, 'response': [{'risetime': 1754487862, 'duration': 241}]}
    assert get_passes(40.027435, 40.027435) == {'request': {'datetime': 1754473147, 'latitude': 40.027435, 'longitude': 40.027435, 'altitude': 0, 'passes': 1}, 'response': [{'risetime': 1754475437, 'duration': 543}]}
    assert mock_api.call_count == 2

def test_get_passes_api_fail(mocker):
    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 400
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=req_mock)
    with pytest.raises(RuntimeError):
        _, _ = get_passes(LONDON_LAT, LONDON_LON)
    assert mock_api.call_count == 1

@pytest.mark.parametrize(
    'args',
    (
        (200, 0),
        (0, 200),
        (-200, 0),
        (0, -200),
        (200, 200),
        (-200, -200)
    )
)
def test_get_passes_bad_input(args):
    with pytest.raises(ValueError):
        get_passes(args[0], args[1])        

@pytest.mark.parametrize(
    'n_param',
    (
        1,
        2,
        3,
        4,
        5
    )
)
@freezegun.freeze_time(STATIC_DATETIME)
def test_present_iss_passes(mocker, tle_fix, n_param):
    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.text = tle_fix
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=req_mock)

    present_list = present_iss_passes(get_passes(LONDON_LAT, LONDON_LON, n=n_param))
    assert len(present_list) == n_param
    assert present_list[0][0] == '2025-08-06 13:44:22+00:00'
    assert present_list[0][1] == 241
    assert mock_api.call_count == 1