# pylint: skip-file
import pandas as pd

from src.transform_weather import transform_current_data, transform_daily_data, transform_hourly_data

current_data = (20.149999618530273, 83.0, 10.440000534057617,
                24.84000015258789, 0.0, 94.0)


def test_transform_current_data():
    result = transform_current_data(current_data)
    assert result[0] == '20.1°C'
    assert result[1] == '83%'
    assert result[2] == '10.4 km/h'
    assert result[3] == '24.8 km/h'
    assert result[4] == '0.0 mm'
    assert result[5] == '94%'


def test_transform_current_data_type():
    result = transform_current_data(current_data)
    assert isinstance(result, tuple)
    assert all(isinstance(x, str) for x in result)


raw_hourly_data = pd.DataFrame({
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


def test_transform_hourly_data_columns():
    result_df = transform_hourly_data(raw_hourly_data)
    expected_columns = [
        "Date", "Temperature (°C)", "Relative Humidity (%)",
        "Wind Speed (km/h)", "Wind Gusts (km/h)",
        "Visibility (km)", "Cloud Cover (%)"
    ]
    assert list(result_df.columns) == expected_columns


def test_transform_hourly_data_values():
    result_df = transform_hourly_data(raw_hourly_data)
    assert result_df.loc[0, "Visibility (km)"] == 10.7
    assert result_df.loc[2, "Cloud Cover (%)"] == 44.0


raw_daily_data = pd.DataFrame({
    "Date": [
        "2025-07-31 00:00:00+00:00",
        "2025-08-01 00:00:00+00:00"
    ],
    "Sunrise": ["2025-07-31 04:23:22", "2025-08-01 04:24:53"],
    "Sunset": ["2025-07-31 19:50:25", "2025-08-01 19:48:34"],
    "Maximum Wind Speed (km/h)": [15.119999, 16.559999],
    "Maximum Wind Gusts (km/h)": [36.360001, 40.680000],
    "Maximum Temperature (°C)": [20.595499, 21.895500],
    "Minimum Temperature (°C)": [16.295500, 15.695499]
})


def test_transform_daily_data_columns():
    result = transform_daily_data(raw_daily_data)
    expected_columns = [
        "Date", "Sunrise", "Sunset",
        "Maximum Wind Speed (km/h)", "Maximum Wind Gusts (km/h)",
        "Maximum Temperature (°C)", "Minimum Temperature (°C)"
    ]
    assert list(result.columns) == expected_columns


def test_transform_daily_data_values():
    result_df = transform_daily_data(raw_daily_data)
    assert result_df.loc[0, "Date"] == "2025-07-31"
    assert result_df.loc[0, "Sunrise"] == "04:23"
    assert result_df.loc[1, "Sunset"] == "19:48"
    assert result_df.loc[0, "Maximum Temperature (°C)"] == 21.3
