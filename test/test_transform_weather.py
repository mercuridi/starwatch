# pylint: skip-file
import pytest
import pandas as pd
from datetime import date

from src transform_weather import transform_current_data, transform_daily_data, transform_hourly_data


@pytest.fixture
def current_data():
    return (
        20.149999618530273, 83.0, 10.440000534057617,
        24.84000015258789, 0.0, 94.0
    )


@pytest.fixture
def raw_hourly_data():
    return pd.DataFrame({
        "Date": [
            "2025-07-31 16:00:00+00:00",
            "2025-07-31 17:00:00+00:00",
            "2025-07-31 18:00:00+00:00"
        ],
        "Temperature (°C)": [20.2955, 20.245501, 20.595499],
        "Relative Humidity (%)": [79.0, 76.0, 73.0],
        "Precipitation (mm)": [0.0, 0.0, 0.0],
        "Wind Speed (km/h)": [12.6, 12.96, 11.88],
        "Wind Gusts (km/h)": [30.96, 32.04, 29.16],
        "Visibility (m)": [10660.0, 14040.0, 14420.0],
        "Cloud Cover (%)": [100.0, 87.0, 44.0]
    })


@pytest.fixture
def raw_daily_data():
    return pd.DataFrame({
        "Date": ["2025-07-31"],
        "Sunrise": ["2025-07-31T05:32:15"],
        "Sunset": ["2025-07-31T20:15:45"],
        "Maximum Wind Speed (km/h)": [18.673],
        "Maximum Wind Gusts (km/h)": [29.147],
        "Maximum Temperature (°C)": [25.449],
        "Minimum Temperature (°C)": [15.286]
    })


def test_transform_current_data(current_data):
    result = transform_current_data(current_data)
    assert result[0] == '20.1°C'
    assert result[1] == '83%'
    assert result[2] == '10.4 km/h'
    assert result[3] == '24.8 km/h'
    assert result[4] == '0.0 mm'
    assert result[5] == '94%'


def test_transform_current_data_type(current_data):
    result = transform_current_data(current_data)
    assert isinstance(result, tuple)
    assert all(isinstance(x, str) for x in result)


def test_transform_hourly_data_columns(raw_hourly_data):
    result_df = transform_hourly_data(raw_hourly_data)
    expected_columns = [
        "Date", "Temperature (°C)", "Relative Humidity (%)",
        "Wind Speed (km/h)", "Wind Gusts (km/h)",
        "Visibility (km)", "Cloud Cover (%)"
    ]
    assert list(result_df.columns) == expected_columns


def test_transform_hourly_data_values(raw_hourly_data):
    result_df = transform_hourly_data(raw_hourly_data)
    assert result_df.loc[0, "Visibility (km)"] == 10.7
    assert result_df.loc[2, "Cloud Cover (%)"] == 44.0


def test_transform_daily_data_columns(raw_daily_data):
    input_daily_data = pd.DataFrame({
        "Date": ["2025-07-31"],
        "Sunrise": ["2025-07-31T05:32:15"],
        "Sunset": ["2025-07-31T20:15:45"],
        "Maximum Wind Speed (km/h)": [18.673],
        "Maximum Wind Gusts (km/h)": [29.147],
        "Maximum Temperature (°C)": [25.449],
        "Minimum Temperature (°C)": [15.286]
    })

    result = transform_daily_data(raw_daily_data)

    expected_columns = [
        "Date", "Sunrise", "Sunset",
        "Maximum Wind Speed (km/h)", "Maximum Wind Gusts (km/h)",
        "Maximum Temperature (°C)", "Minimum Temperature (°C)"
    ]
    assert list(result.columns) == expected_columns


def test_transform_daily_data_values(raw_daily_data):
    result = transform_daily_data(raw_daily_data)

    assert result.loc[0, "Date"] == date(2025, 7, 31)
    assert result.loc[0, "Sunrise"] == "05:32"
    assert result.loc[0, "Sunset"] == "20:15"
    assert result.loc[0, "Maximum Wind Speed (km/h)"] == 18.7
    assert result.loc[0, "Maximum Wind Gusts (km/h)"] == 29.1
    assert result.loc[0, "Maximum Temperature (°C)"] == 25.4
    assert result.loc[0, "Minimum Temperature (°C)"] == 15.3
