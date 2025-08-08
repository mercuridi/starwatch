import pytest
from unittest.mock import MagicMock, patch
from src.moon_phase_extract import get_moon_phase_image
from src.astronomy_utils import make_request_headers


@patch('requests.post')
@patch('requests.get')
def test_moon_phase_image_successfully_retrieved(mock_get, mock_post):
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = {
        'data': {
            'imageUrl': 'https://fakeurl.com/moon.jpg'
        }
    }
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.content = b'fake_image_data'
    mock_get.return_value = mock_get_response

    lat = 0.05
    lon = 0.14
    date = '2025-03-02'
    moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"

    result = get_moon_phase_image(
        lat, lon, date, {}, moon_phase_url)
    assert isinstance(result, bytes)
    assert result == b'fake_image_data'


@patch("requests.post")
def test_moon_phase_calls_api(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {'imageUrl': 'https://fake.com/image.jpg'}}

    with patch("requests.get") as mock_get:
        mock_get.return_value.content = b'image_data'
        moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
        get_moon_phase_image(0.05, 0.14, '2025-03-02',
                             {}, moon_phase_url)
        mock_post.assert_called_once()


def test_moon_phase_image_invalid():
    moon_phase_url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
    result = get_moon_phase_image(
        0.05, 0.14, '20i25-03-02', {}, moon_phase_url)
    assert isinstance(result, str)
    assert 'Error' in result
