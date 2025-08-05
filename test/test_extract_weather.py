# pylint: skip-file

from unittest.mock import MagicMock
import pytest
import pandas as pd
from datetime import datetime, timedelta
from freezegun import freeze_time

from src.extract_weather import (get_response, process_current_data, 
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



@freeze_time("2025-08-01 00:00:00")
def test_process_hourly_data_returns_dataframe_with_correct_len():
    mock_response = MagicMock()
    mock_hourly = MagicMock()

    mock_response.Hourly.return_value = mock_hourly

    # To control the hourly_data time data
    example_time = datetime(2025, 8, 1, 0, 0, 0)
    mock_hourly.Time.return_value = example_time.timestamp()
    mock_hourly.TimeEnd.return_value = (
        example_time + timedelta(hours=24)).timestamp()
    mock_hourly.Interval.return_value = 3600  # seconds in an hour

    # Provide example data for variable output
    mock_variable = MagicMock()
    example_hourly_output = list(range(24))
    mock_variable.ValuesAsNumpy.return_value = example_hourly_output
    mock_hourly.Variables.side_effect = lambda i: mock_variable
    
    hourly_data = process_hourly_data(mock_response)

    assert isinstance(hourly_data, pd.DataFrame)
    assert len(hourly_data) == 24



def test_process_hourly_data_correct_columns():
    mock_response = MagicMock()
    mock_hourly = MagicMock()

    mock_response.Hourly.return_value = mock_hourly

    # To control the hourly_data time data
    example_time = datetime(2025, 8, 1, 0, 0, 0)
    mock_hourly.Time.return_value = example_time.timestamp()
    mock_hourly.TimeEnd.return_value = (
        example_time + timedelta(hours=24)).timestamp()
    mock_hourly.Interval.return_value = 3600  # seconds in an hour

    # Provide example data for variable output
    mock_variable = MagicMock()
    example_hourly_output = list(range(24))
    mock_variable.ValuesAsNumpy.return_value = example_hourly_output
    mock_hourly.Variables.side_effect = lambda i: mock_variable

    hourly_data = process_hourly_data(mock_response)

    assert all(hourly_data.columns == ["Date", "Temperature (°C)", "Relative Humidity (%)", "Precipitation (mm)", "Wind Speed (km/h)", "Wind Gusts (km/h)", "Visibility (m)", "Cloud Cover (%)"])



def test_process_hourly_data_runtime_error():
    mock_response = MagicMock()
    mock_hourly = MagicMock()

    mock_hourly.Variables.side_effect = RuntimeError(
        "Unable to return hourly weather data")

    with pytest.raises(RuntimeError):
        process_hourly_data(mock_response)



def test_convert_unix_timestamp():
    assert convert_unix_timestamp(1754301848) == "2025-08-04 10:04:08"


def test_convert_unix_timestamp_from_start():
    assert convert_unix_timestamp(0) == "1970-01-01 00:00:00"


def test_process_daily_data_returns_dataframe_with_correct_len():
    mock_response = MagicMock()
    mock_daily = MagicMock()
    mock_response.Daily.return_value = mock_daily

    # To control the daily_data time data
    example_time = datetime(2025, 8, 1, 0, 0, 0)
    mock_daily.Time.return_value = example_time.timestamp()
    mock_daily.TimeEnd.return_value = (
        example_time + timedelta(days=7)).timestamp()
    mock_daily.Interval.return_value = 86400  # seconds in a day

    # Fixed time to use for both sunrise and sunset
    example_time = [datetime(2025, 8, 1, 13, 0, 0).timestamp()] * 7

    # Example data for the remaining columns
    remaining_example_values = list(range(7))

    # Mock return values for ValuesInt64AsNumpy and ValuesAsNumpy separately
    mock_variable_0 = MagicMock()
    mock_variable_0.ValuesInt64AsNumpy.return_value = example_time
    mock_remaining = MagicMock()
    mock_remaining.ValuesAsNumpy.return_value = remaining_example_values

    # Assign return values to side effect for different variable types
    mock_daily.Variables.side_effect = lambda i: mock_variable_0 if i == 0 or i == 1 else mock_remaining

    daily_data = process_daily_data(mock_response)

    assert isinstance(daily_data, pd.DataFrame)
    assert len(daily_data) == 7



def test_process_daily_data_correct_columns():
    mock_response = MagicMock()
    mock_daily = MagicMock()
    mock_response.Daily.return_value = mock_daily

    # To control the daily_data time data
    example_time = datetime(2025, 8, 1, 0, 0, 0)
    mock_daily.Time.return_value = example_time.timestamp()
    mock_daily.TimeEnd.return_value = (
        example_time + timedelta(days=7)).timestamp()
    mock_daily.Interval.return_value = 86400   # seconds in a day

    # Fixed time to use for both sunrise and sunset
    example_time = [datetime(2025, 8, 1, 13, 0, 0).timestamp()] * 7

    # Example data for the remaining columns
    remaining_example_values = list(range(7))

    # Mock return values for ValuesInt64AsNumpy and ValuesAsNumpy separately
    mock_variable_0_and_1 = MagicMock()
    mock_variable_0_and_1.ValuesInt64AsNumpy.return_value = example_time
    mock_remaining = MagicMock()
    mock_remaining.ValuesAsNumpy.return_value = remaining_example_values

    # Assign return values to side effect for different variable types
    mock_daily.Variables.side_effect = lambda i: mock_variable_0_and_1 if i == 0 or i == 1 else mock_remaining

    daily_data = process_daily_data(mock_response)

    assert all(daily_data.columns == ["Date", "Sunrise",
                                  "Sunset", "Maximum Wind Speed (km/h)", "Maximum Wind Gusts (km/h)", "Maximum Temperature (°C)", "Minimum Temperature (°C)"])



def test_process_daily_data_runtime_error():
    mock_response = MagicMock()
    mock_daily = MagicMock()

    mock_daily.Variables.side_effect = RuntimeError(
        "Unable to return daily weather data")

    with pytest.raises(RuntimeError):
        process_daily_data(mock_response)
