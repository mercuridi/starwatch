"""Dashboard script"""

import sys
import os
from datetime import datetime

import openmeteo_requests
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, Engine
from dotenv import load_dotenv


sys.path.append('../')
from src.extract_weather import (get_client, get_response,
                                 process_current_data, process_hourly_data,
                                 process_daily_data)
from src.transform_weather import (transform_current_data, transform_hourly_data,
                                   transform_daily_data)


def create_regions_dataframe():
    """Returns dataframe containing lat/long pairs for all regions of the UK"""

    # lat/long pairs snatched from Wikipedia
    regions = {
        "region_name": [
            "Cymru Wales",
            "East Midlands",
            "East of England",
            "London",
            "North East & Cumbria",
            "North West",
            "Northern Ireland",
            "Scotland",
            "South East",
            "South West",
            "West Midlands",
            "Yorkshire & the Humber"
        ],
        "latitude": [
            +51.29,  # Wales (actually Cardiff)
            +52.98,  # East Midlands
            +52.24,  # East of England
            +51.30,  # London (actually City of London)
            +55.00,  # North East & Cumbria
            +54.04,  # North West
            +54.60,  # Northern Ireland (actually Belfast)
            +55.57,  # Scotland (actually Edinburgh)
            +51.30,  # South East
            +50.96,  # South West
            +52.28,  # West Midlands
            +53.34  # Yorkshire & the Humber
        ],
        "longitude": [
            -03.11,  # Wales (actually Cardiff)
            -00.75,  # East Midlands
            +00.41,  # East of England
            -00.05,  # London (actually City of London)
            -01.87,  # North East & Cumbria
            -02.45,  # North West
            -05.93,  # Northern Ireland (actually Belfast)
            -03.11,  # Scotland (actually Edinburgh)
            -00.80,  # South East
            -03.22,  # South West
            -02.15,  # West Midlands
            -01.12  # Yorkshire & the Humber
        ]
    }
    return pd.DataFrame(data=regions)



def create_response_for_region(region_name: str, regions: pd.DataFrame,
                               weather_client: openmeteo_requests.Client) -> WeatherApiResponse:
    """Returns Ocean-Meteo API response, provided with a region name, a region dataframe (containing 
    latitude and longitude pairs for each region), and an Open-Meteo requests client.
    """

    region_lat_long = regions[regions["region_name"] == region_name]
    region_latitude = region_lat_long["latitude"].values[0]
    region_longitude = region_lat_long["longitude"].values[0]

    return get_response(
        latitude=region_latitude, longitude=region_longitude, client=weather_client)



def display_current_weather_metrics(current_data: tuple[str], daily_data: pd.DataFrame) -> None:
    """Displays streamlit metrics for current weather statistics"""

    sunrise = str(daily_data["Sunrise"][0]) + "am"
    sunset  = str(daily_data["Sunset"][0]) + "pm"

    a, b, c, d = st.columns(4)
    e, f, g, h = st.columns(4)

    a.metric("Temperature", current_data[0], border=True)
    b.metric("Cloud Cover", current_data[5], border=True)
    c.metric("Relative Humidity", current_data[1], border=True)
    d.metric("Precipitation", current_data[4], border=True)
    e.metric("Wind Speed", current_data[2], border=True)
    f.metric("Wind Gusts", current_data[3], border=True)
    g.metric("Sunrise", sunrise, border=True)
    h.metric("Sunset", sunset, border=True)



def display_hourly_graphs(hourly_data: pd.DataFrame) -> None:
    """Displays selectable graphs for hourly weather data"""

    option = st.selectbox("Select an option:", ["Temperature", "Cloud Cover",
                                                "Relative Humidity", "Visibility",
                                                "Wind Speed", "Wind Gusts"])
    if option == "Temperature":
        st.line_chart(hourly_data, x="Date", y="Temperature (°C)", x_label="Time")
    if option == "Relative Humidity":
        st.line_chart(hourly_data, x="Date",
                      y="Relative Humidity (%)", x_label="Time")
    if option == "Wind Speed":
        st.line_chart(hourly_data, x="Date",
                      y="Wind Speed (km/h)", x_label="Time")
    if option == "Wind Gusts":
        st.line_chart(hourly_data, x="Date",
                      y="Wind Gusts (km/h)", x_label="Time")
    if option == "Visibility":
        st.line_chart(hourly_data, x="Date",
                      y="Visibility (km)", x_label="Time")
    if option == "Cloud Cover":
        st.line_chart(hourly_data, x="Date",
                      y="Cloud Cover (%)", x_label="Time")



def display_daily_graphs(daily_data: pd.DataFrame) -> None:
    """Displays selectable graphs for daily averages for weather data spanning one week"""

    option = st.selectbox("Select an option:", ["Maximum Wind Speed", "Maximum Wind Gust",
                                                "Maximum Temperature", "Minimum Temperature",
                                                "Sunrise", "Sunset"])
    if option == "Maximum Wind Speed":
        st.line_chart(daily_data, x="Date",
                      y="Maximum Wind Speed (km/h)")
    if option == "Maximum Wind Gust":
        st.line_chart(daily_data, x="Date",
                      y="Maximum Wind Gusts (km/h)")
    if option == "Maximum Temperature":
        st.line_chart(daily_data, x="Date",
                      y="Maximum Temperature (°C)")
    if option == "Minimum Temperature":
        st.line_chart(daily_data, x="Date",
                      y="Minimum Temperature (°C)")
    if option == "Sunrise":
        st.scatter_chart(daily_data, x="Date",
                      y="Sunrise")
    if option == "Sunset":
        st.scatter_chart(daily_data, x="Date",
                         y="Sunset")


def weather_section() -> None:
    """Weather section of the dashboard, with selectable region"""""

    st.subheader("Region Selection :world_map:", divider="blue")
    regions_df = create_regions_dataframe()
    region_option = st.selectbox("Select a region:", ["Cymru Wales", "East Midlands",
                                                      "East of England", "London",
                                                      "North East & Cumbria", "North West",
                                                      "Northern Ireland", "Scotland",
                                                      "South East", "South West",
                                                      "West Midlands", "Yorkshire & the Humber"])

    # Cache weather data for 15 minutes
    weather_client = get_client(cache_expiry=900)
    weather_response = create_response_for_region(
        region_option, regions_df, weather_client)

    # Extract and transform data
    extract_current_weather = process_current_data(weather_response)
    extract_hourly_weather = process_hourly_data(weather_response)
    extract_daily_weather = process_daily_data(weather_response)

    transform_current_weather = transform_current_data(extract_current_weather)
    transform_hourly_weather = transform_hourly_data(extract_hourly_weather)
    transform_daily_weather = transform_daily_data(extract_daily_weather)

    st.subheader("Current Weather Stats", divider="blue")
    display_current_weather_metrics(
        transform_current_weather, transform_daily_weather)

    st.subheader("24 Hour Weather Forecast", divider="blue")
    display_hourly_graphs(transform_hourly_weather)

    st.subheader("Weekly Weather Forecast", divider="blue")
    display_daily_graphs(transform_daily_weather)



def get_db_connection() -> Engine:
    """Establish and returns connection to DB"""
    load_dotenv()
    db_username = os.getenv("db_username")
    db_password = os.getenv("db_password")
    db_name = os.getenv("db_name")
    db_port = os.getenv("db_port")
    db_host = os.getenv("db_host")

    # String concatenation for connection url
    url = (
        f"postgresql+psycopg2://{db_username}:{db_password}"
        + f"@{db_host}:{db_port}/{db_name}"
    )
    return create_engine(url)


def get_rds_data(engine: Engine, table_name: str):
    """Connects to RDS database and returns data corresponding to the table name
    entered.
    """
    with engine.connect() as conn:
        rds_data = conn.execute(
            text(f"SELECT * FROM {table_name}")).fetchall()
    return rds_data



def get_all_data(engine: Engine) -> pd.DataFrame:
    """Returns all relevant data from the database to be displayed in the dashboard"""

    # Query database to select all data from each table
    distance_df = pd.DataFrame(get_rds_data(engine, "distance"))
    planetary_body_df = pd.DataFrame(get_rds_data(engine, "planetary_body"))
    forecast_df = pd.DataFrame(get_rds_data(engine, "forecast"))
    constellation_df = pd.DataFrame(get_rds_data(engine, "constellation"))

    # Merge table
    distance_pb = pd.merge(
        distance_df, planetary_body_df, on="planetary_body_id")
    distance_pb_forecast = pd.merge(
        distance_pb, forecast_df, on=["planetary_body_id", "date"])
    all_data = pd.merge(distance_pb_forecast,
                        constellation_df, on="constellation_id")

    return all_data[["planetary_body_name", "date", "constellation_name",
                     "astronomical_units", "right_ascension_hours", "right_ascension_string",
                     "declination_degrees", "declination_string", "altitude_degrees",
                     "altitude_string", "azimuth_degrees", "azimuth_string"]]



def select_planetary_body_metrics(data: pd.DataFrame) -> None:
    """Displays metrics for a selectable planetary body"""

    st.subheader("Planetary Positions :telescope:", divider="blue")
    planetary_body_option = st.selectbox("Select a planetary body:", ["Sun", "Moon",
                                                                      "Mercury", "Venus",
                                                                      "Earth", "Mars",
                                                                      "Jupiter", "Saturn",
                                                                      "Uranus", "Neptune",
                                                                      "Pluto"])

    pb_data = data[data["planetary_body_name"] == planetary_body_option]
    
    pb_data_specific_date = pb_data[pb_data["date"] == "2025-08-07"]
    # change date to today once db is updated
    today = datetime.today().strftime("%Y-%m-%d")
    # pb_data_today = = pb_data[pb_data["date"] == today]

    a, b = st.columns(2)

    a.metric("Distance from Earth",
             str(pb_data_specific_date["astronomical_units"].iloc[0]) + " AU", border=True)
    b.metric("Constellation",
             pb_data_specific_date["constellation_name"].iloc[0], border=True)


    equatorial = pb_data[["date", "right_ascension_string", "declination_string"]]
    equatorial.rename(
        columns={"right_ascension_string": "Right Ascension", "declination_string": "Declination"}, inplace=True)

    equatorial["date"] = equatorial["date"].dt.strftime("%Y-%m-%d")
    transpose_equatorial = equatorial.transpose()

    header = transpose_equatorial.iloc[0]
    transpose_equatorial = transpose_equatorial[1:]
    transpose_equatorial.columns = header
    st.markdown("##### Equatorial co-ordinates:")
    st.table(transpose_equatorial)

    horizontal = pb_data[["date", "altitude_string", "azimuth_string"]]
    horizontal.rename(
        columns={"altitude_string": "Altitude", "azimuth_string": "Azimuth"}, inplace=True)

    horizontal["date"] = horizontal["date"].dt.strftime("%Y-%m-%d")
    transpose_horizontal = horizontal.transpose()

    header = transpose_horizontal.iloc[0]
    transpose_horizontal = transpose_horizontal[1:]
    transpose_horizontal.columns = header

    st.markdown("##### Horizontal co-ordinates:")
    st.table(transpose_horizontal)



def main():
    """Main function"""

    st.title(":night_with_stars: :sparkles: StarWatch :sparkles: :milky_way:")

    engine = get_db_connection()
    planetary_data = get_all_data(engine)
    select_planetary_body_metrics(planetary_data)

    st.header(
        ":waning_crescent_moon: :last_quarter_moon: :waning_gibbous_moon: "
        ":full_moon: :waxing_gibbous_moon: :first_quarter_moon: :waxing_crescent_moon: "
        ":new_moon: :waning_crescent_moon: :last_quarter_moon: :waning_gibbous_moon: " \
        ":full_moon: :waxing_gibbous_moon: :first_quarter_moon: :waxing_crescent_moon:")

    weather_section()



if __name__ == "__main__":
    main()
    # engine = get_db_connection()
    # all_data = get_all_data(engine)
