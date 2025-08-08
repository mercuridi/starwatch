# pylint: skip-file
from unittest.mock import MagicMock
import requests
import pytest


from src.extract_nasa import get_image_details, get_neos

# Tests get_image_details


def test_get_image_details_correct_return_values(mocker):
    api_data = {"title": "test_title",
                "explanation": "test_explanation",
                "url": "test_image_url",
                "media_type": "image"}

    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.json = MagicMock(return_value=api_data)
    mock_api = mocker.patch(__name__ + ".requests.get",
                            return_value=req_mock)

    title, explanation, image_url = get_image_details(None, None)

    assert mock_api.call_count == 1
    assert title == "test_title"
    assert explanation == "test_explanation"
    assert image_url == "test_image_url"


def test_get_image_details_not_image_error(mocker):
    api_data = {"title": "test_title",
                "explanation": "test_explanation",
                "url": "test_image_url",
                "media_type": "not_image"}

    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.json = MagicMock(return_value=api_data)
    mocker.patch("src.extract_nasa.reqs.get", return_value=req_mock)

    with pytest.raises(ValueError) as exc_info:
        get_image_details("fake_url", {})

    assert "Today's APOD is not an image." in str(exc_info.value)


def test_get_image_details_runtime_error(mocker):
    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 500
    req_mock.text = "Internal Server Error"
    mocker.patch("src.extract_nasa.reqs.get", return_value=req_mock)

    with pytest.raises(RuntimeError) as exc_info:
        get_image_details("fake_url", {})

    assert "Failed to fetch APOD data" in str(exc_info.value)
    assert "500" in str(exc_info.value)

# Tests get_neos


def test_get_neos_raises_error(mocker):
    today = "2025-05-23"

    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 500
    req_mock.text = "Internal Server Error"
    mocker.patch("src.extract_nasa.reqs.get", return_value=req_mock)

    with pytest.raises(RuntimeError) as exc_info:
        get_image_details("fake_url", {"param": "value"})

    assert "Failed to fetch NEO data" in str(exc_info.value)
    assert "500" in str(exc_info.value)


def test_get_neos_correct_return_values(mocker):
    api_data = {
        "near_earth_objects": {
            "2025-05-23": [
                {
                    "name": "(example neo)",
                    "estimated_diameter": {
                        "meters": {
                            "estimated_diameter_min": 725.472,
                            "estimated_diameter_max": 867.253
                        }
                    },
                    "is_potentially_hazardous_asteroid": False,
                    "close_approach_data": [
                        {
                            "miss_distance": {"kilometers": "632.0"},
                            "relative_velocity": {"kilometers_per_hour": "3657.0"}
                        }
                    ]
                }
            ]
        }
    }

    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.json = MagicMock(return_value=api_data)
    mock_api = mocker.patch(
        "src.extract_nasa.reqs.get", return_value=req_mock)

    neos = get_neos("fake_url", {"param": "value"}, "2025-05-23")

    assert neos[0]["name"] == "example neo"
    assert neos[0]["diameter_min_m"] == 725.5
    assert neos[0]["diameter_max_m"] == 867.3
    assert neos[0]["hazardous"] is False
    assert neos[0]["miss_distance_km"] == 632.0
    assert neos[0]["relative_velocity_kmph"] == 3657.0
    assert mock_api.call_count == 1


def test_get_neos_raises_error(mocker):
    today = "2025-05-23"

    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 500
    req_mock.text = "Internal Server Error"
    mocker.patch("src.extract_nasa.reqs.get", return_value=req_mock)

    with pytest.raises(RuntimeError) as exc_info:
        get_neos("fake_url", {"param": "value"}, today)

    assert "Failed to fetch NEO data" in str(exc_info.value)
    assert "500" in str(exc_info.value)


def test_get_neos_returns_empty_list(mocker):
    today = "2025-05-23"
    api_data = {"near_earth_objects": {today: []}}

    req_mock = MagicMock(spec=requests.Response)
    req_mock.status_code = 200
    req_mock.json.return_value = api_data
    mocker.patch("src.extract_nasa.reqs.get", return_value=req_mock)

    result = get_neos("fake_url", {}, today)
    assert result == []
