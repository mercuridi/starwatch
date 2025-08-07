from src.moon_phase_extract import get_moon_phase_image
from src.astronomy_utils import make_request_headers
import pytest
from unittest.mock import MagicMock, patch


def test_moon_phase_image_gotten():
    lat = 0.05
    lon = 0.14
    date = '2025-03-02'
    moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
    assert isinstance(get_moon_phase_image(
        lat, lon, date, make_request_headers(), moon_phase_url), bytes)


@patch("requests.post")
def test_moon_phase_calls_api(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'key': 'value'}
    moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
    get_moon_phase_image(0.05, 0.14, '2025-03-02',
                         make_request_headers(), moon_phase_url)
    mock_post.assert_called_once


def test_moon_phase_image_invalid():
    moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
    print(get_moon_phase_image(0.05, 0.14, '20i25-03-02',
                                           make_request_headers(), moon_phase_url))
    assert 'Error' in get_moon_phase_image(0.05, 0.14, '202i5-03-02',
                                           make_request_headers(), moon_phase_url)
