"""Transform script for the Open-Meteo API data"""

import pandas as pd

from extract_weather import get_client, get_response, process_current_data, process_daily_data, process_hourly_data


def transform_current_data(data: tuple[float]) -> tuple[str]:
    """Rounds each measurement and returns values as tuple of strings, with correct units"""

    # Rounds each measurement appropriately
    current_temperature = round(data[0], 1)
    current_relative_humidity = int(data[1])
    current_wind_speed = round(data[2], 1)
    current_wind_gusts = round(data[3], 1)
    current_precipitation = round(data[4], 1)
    current_cloud_cover = int(data[5])

    return (f"{current_temperature}°C", f"{current_relative_humidity}%",
            f"{current_wind_speed} km/h", f"{current_wind_gusts} km/h",
            f"{current_precipitation} mm", f"{current_cloud_cover}%")


def transform_hourly_data(data: pd.DataFrame) -> pd.DataFrame:
    """Returns transformed hourly data dataframe"""

    # Rounds each measurement to 1 d.p.
    data["Temperature (°C)"] = data["Temperature (°C)"].astype(float).round(1)
    data["Wind Speed (km/h)"] = data["Wind Speed (km/h)"].astype(float).round(1)
    data["Wind Gusts (km/h)"] = data["Wind Gusts (km/h)"].astype(float).round(1)

    # Converts to integers as all values end with '.0'
    data["Relative Humidity (%)"] = data["Relative Humidity (%)"].astype(int)
    data["Cloud Cover (%)"] = data["Cloud Cover (%)"].astype(int)

    # Converts visibility units from metres to kilometres
    data["Visibility (m)"] = data["Visibility (m)"]
    data["Visibility (km)"] = (data["Visibility (m)"] /
                               1000).astype(float).round(1)

    return data[["Date", "Temperature (°C)", "Relative Humidity (%)",
                 "Wind Speed (km/h)", "Wind Gusts (km/h)",
                 "Visibility (km)", "Cloud Cover (%)"]]


def transform_daily_data(data: pd.DataFrame) -> pd.DataFrame:
    """Returns transformed daily data dataframe"""

    data["Date"] = pd.to_datetime(data["Date"]).dt.date

    # Converts string to datetime then extracts time without seconds
    data["Sunrise"] = pd.to_datetime(data["Sunrise"]).dt.strftime("%H:%M")
    data["Sunset"] = pd.to_datetime(data["Sunset"]).dt.strftime("%H:%M")

    # Rounds each measurement to 1 d.p.
    data["Maximum Wind Speed (km/h)"] = data["Maximum Wind Speed (km/h)"].astype(
        float).round(1)
    data["Maximum Wind Gusts (km/h)"] = data["Maximum Wind Gusts (km/h)"].astype(
        float).round(1)
    data["Maximum Temperature (°C)"] = data["Maximum Temperature (°C)"].astype(
        float).round(1)
    data["Minimum Temperature (°C)"] = data["Minimum Temperature (°C)"].astype(
        float).round(1)

    return data
