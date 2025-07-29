"""Extract script for the Open-Meteo API"""

from datetime import datetime, UTC
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def get_client(cache_expiry: int) -> openmeteo_requests.Client:
    """Returns Open-Meteo requests client"""
    cache_session = requests_cache.CachedSession(
        '.cache', expire_after=cache_expiry)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    return openmeteo_requests.Client(session=retry_session)


def get_response(latitude: float, longitude: float, client: openmeteo_requests.Client):
    """Returns a response, provided with latitude, longitude, and an Open-Meteo requests client"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["sunrise", "sunset", "wind_speed_10m_max", "wind_gusts_10m_max",
                  "temperature_2m_max", "temperature_2m_min"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation",
                   "wind_speed_10m", "wind_gusts_10m", "visibility", "cloud_cover",
                   "surface_pressure", "pressure_msl"],
        "models": "ukmo_seamless",
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m",
                    "wind_gusts_10m", "precipitation", "cloud_cover"],
        "timezone": "GMT",
        "forecast_days": 7,
    }
    return client.weather_api(url, params=params)[0]


def process_current_data(response):
    """Prints current weather data from the API response"""
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_wind_speed_10m = current.Variables(2).Value()
    current_wind_gusts_10m = current.Variables(3).Value()
    current_precipitation = current.Variables(4).Value()
    current_cloud_cover = current.Variables(5).Value()

    print(
        f"\nCurrent time: {datetime.fromtimestamp(current.Time(),
                                                  UTC).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current temperature_2m: {current_temperature_2m}")
    print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
    print(f"Current wind_speed_10m: {current_wind_speed_10m}")
    print(f"Current wind_gusts_10m: {current_wind_gusts_10m}")
    print(f"Current precipitation: {current_precipitation}")
    print(f"Current cloud_cover: {current_cloud_cover}")


def process_hourly_data(response) -> pd.DataFrame:
    """Returns a dataframe containing 24 hours of weather information starting from 
    the current hour, from an API response.
    """
    hourly = response.Hourly()
    hourly_data = {"Date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["Temperature (°C)"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["Relative Humidity (%)"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["Precipitation (mm)"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["Wind Speed (km/h)"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_data["Wind Gusts (km/h)"] = hourly.Variables(4).ValuesAsNumpy()
    hourly_data["Visibility (m)"] = hourly.Variables(5).ValuesAsNumpy()
    hourly_data["Cloud Cover (%)"] = hourly.Variables(6).ValuesAsNumpy()

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    current_hour = datetime.now().hour
    return hourly_dataframe.iloc[current_hour:current_hour+24]


def convert_unix_timestamp(unix_timestamp: int) -> str:
    """Returns unix timestamp as a datetime string"""
    return datetime.fromtimestamp(
        unix_timestamp, UTC).strftime('%Y-%m-%d %H:%M:%S')


def process_daily_data(response):
    """Returns a dataframe for daily averages of weather data from an API response"""
    daily = response.Daily()
    daily_data = {"Date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["Sunrise"] = daily.Variables(0).ValuesInt64AsNumpy()
    daily_data["Sunset"] = daily.Variables(1).ValuesInt64AsNumpy()
    daily_data["Maximum Wind Speed (km/h)"] = daily.Variables(2).ValuesAsNumpy()
    daily_data["Maximum Wind Gusts (km/h)"] = daily.Variables(3).ValuesAsNumpy()
    daily_data["Maximum Temperature (°C)"] = daily.Variables(4).ValuesAsNumpy()
    daily_data["Minimum Temperature (°C)"] = daily.Variables(5).ValuesAsNumpy()

    df = pd.DataFrame(data=daily_data)
    df["Sunrise"] = df["Sunrise"].apply(
        convert_unix_timestamp)
    df["Sunset"] = df["Sunset"].apply(convert_unix_timestamp)
    return df


def main():
    """Main function"""
    client = get_client(3600)
    response = get_response(51.5085, -0.1257, client)

    process_current_data(response)
    print(process_hourly_data(response))
    print(process_daily_data(response))


if __name__ == "__main__":
    main()
