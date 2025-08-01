# pylint: skip-file

from unittest.mock import MagicMock
import pytest
import pandas as pd
from datetime import datetime, timedelta

from src.extract_weather import (get_client, get_response, process_current_data, 
                                 process_hourly_data, process_daily_data, convert_unix_timestamp)



def test_get_response_mock_client():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_client.weather_api.return_value = [mock_response]

    response = get_response(51.29, -03.11, mock_client)

    mock_client.weather_api.assert_called_once()
    assert response == mock_response


def test_get_response_mock_client_runtime_error():
    mock_client = MagicMock()
    mock_client.weather_api.side_effect = RuntimeError("Unable to return client")

    with pytest.raises(RuntimeError):
        get_response(29, -03.11, mock_client)



def test_process_current_data_returns_tuple_correct_len():
    mock_response = MagicMock()
    current_data = process_current_data(mock_response)
    assert isinstance(current_data, tuple)
    assert len(current_data) == 6



def test_process_current_data_correct_variable():
    mock_response = MagicMock()
    mock_current = MagicMock()

    mock_variable_0 = MagicMock()
    mock_variable_0.Value.return_value = 17.53

    current_variable_values = lambda i: mock_variable_0 if i == 0 else MagicMock()

    mock_current.Variables.side_effect = current_variable_values
    mock_response.Current.return_value = mock_current

    current_data = process_current_data(mock_response)

    assert current_data[0] == 17.53
    assert isinstance(current_data[1], MagicMock)


def test_process_current_data_runtime_error():
    mock_response = MagicMock()
    mock_current = MagicMock()

    mock_current.Variables.side_effect = RuntimeError("Unable to return current weather data")
    mock_response.Current.return_value = mock_current

    with pytest.raises(RuntimeError):
        process_current_data(mock_response)

