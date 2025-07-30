"""Dashboard script"""

import sys
sys.path.append('../')

import streamlit as st
import pandas as pd

from src.extract_weather import get_client, get_response, process_current_data, process_hourly_data, process_daily_data
from src.transform_weather import transform_current_data, transform_hourly_data, transform_daily_data


def display_current_weather_metrics(current_data: tuple[str]) -> None:
    temperature       = current_data[0]
    cloud_cover       = current_data[5]
    relative_humidity = current_data[1]
    precipitation     = current_data[4]
    wind_speed        = current_data[2]
    wind_gusts        = current_data[3]

    a, b, c = st.columns(3)
    d, e, f = st.columns(3)

    a.metric("Temperature", temperature, border=True)
    b.metric("Cloud Cover", cloud_cover, border=True)
    c.metric("Relative Humidity", relative_humidity, border=True)
    d.metric("Precipitation", precipitation, border=True)
    e.metric("Wind Speed", wind_speed, border=True)
    f.metric("Wind Gusts", wind_gusts, border=True)

def display_hourly_graphs(hourly_data:pd.DataFrame) -> None:
    option = st.selectbox("Select an option:", ["Temperature", "Cloud Cover",
                                                "Relative Humidity", "Visibility",
                                                "Wind Speed", "Wind Gusts"])
    if option == "Temperature":
        st.line_chart(hourly_data, x="Date", y="Temperature (°C)")
    if option == "Relative Humidity":
        st.line_chart(hourly_data, x="Date", y="Relative Humidity (%)")
    if option == "Wind Speed":
        st.line_chart(hourly_data, x="Date", y="Wind Speed (km/h)")
    if option == "Wind Gusts":
        st.line_chart(hourly_data, x="Date", y="Wind Gusts (km/h)")
    if option == "Visibility":
        st.line_chart(hourly_data, x="Date", y="Visibility (km)")
    if option == "Cloud Cover":
        st.line_chart(hourly_data, x="Date", y="Cloud Cover (%)")



if __name__ == "__main__":
    st.title("StarWatch")

    # cache weather data for 15 minutes
    weather_client = get_client(cache_expiry=900)
    # example coordinates
    weather_response = get_response(latitude=50, longitude=-1.2, client=weather_client)

    # Extract
    extract_current_weather = process_current_data(weather_response)
    extract_hourly_weather  = process_hourly_data(weather_response)
    extract_daily_weather   = process_daily_data(weather_response)

    # Transform
    transform_current_weather = transform_current_data(extract_current_weather)
    transform_hourly_weather  = transform_hourly_data(extract_hourly_weather)
    transform_daily_weather   = transform_daily_data(extract_daily_weather)

    st.subheader("Current Weather Stats", divider=True)
    display_current_weather_metrics(transform_current_weather)

    st.subheader("24 Hour Weather Forecast", divider=True)
    display_hourly_graphs(transform_hourly_weather)