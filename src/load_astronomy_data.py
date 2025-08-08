'''
Loads transformed data
Gets planetary body, and constellation ids from the RDS and maps this to the corresponding data
Transforms data into 2 dataframes, one for each table insertion in RDS
Loads these tables into forecast and distance tables in RDS
'''
from src.transform_astronomy_data import get_json_data, filter_data
import os
from typing import Tuple

from sqlalchemy import create_engine, text, Engine
import pandas as pd
from dotenv import load_dotenv
import logging

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


FILE_PATH = "../data/planetary_data.json"


def get_db_connection() -> Engine:
    '''Establish and returns connection to DB'''
    db_username = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")
    db_host = os.getenv("DB_HOST")

    # String concatenation for connection url
    url = (
        f"postgresql+psycopg2://{db_username}:{db_password}"
        + f"@{db_host}:{db_port}/{db_name}"
    )
    logging.info("Connection Established for RDS")
    return create_engine(url)


def get_transformed_data() -> pd.DataFrame:
    '''Loads and transforms data into a dataframe, functionality from transform script'''
    transformed_data = filter_data(get_json_data(FILE_PATH))
    return transformed_data


def get_ids_from_database(engine: Engine) -> Tuple[dict, dict]:
    '''Gets planetary body id and constellation ids as a dictionary, returns for mapping'''
    with engine.connect() as conn:
        planetary_body = conn.execute(
            text("SELECT * FROM planetary_body")).fetchall()
        constellations = conn.execute(
            text("SELECT constellation_id, constellation_name FROM constellation")
        ).fetchall()

    # Creates a dictionary to allow mapping to corresponding ids for schema compatibility
    planetary_body_dict = {name: id for id, name in planetary_body}
    constellation_dict = {name: id for id, name in constellations}
    return planetary_body_dict, constellation_dict


def add_ids_to_dataframe(
        data: pd.DataFrame,
        planetary_body_mappings: dict,
        constellation_mappings: dict
) -> pd.DataFrame:
    '''
    Add id column for planetary body and constellation data in dataframe
    Maps id to its relevant values
    '''

    # Creates id col for constellation & planetary_body, maps ids from values
    data['constellation_id'] = data['constellation'].map(
        constellation_mappings)
    data['planetary_body_id'] = data['planetary_body'].map(
        planetary_body_mappings)
    return data


def convert_types(data: pd.DataFrame) -> pd.DataFrame:
    '''Convert data types for schema compatiblity'''

    for col in data.columns:
        if col.endswith('_string'):
            data[col] = data[col].astype('string')
        elif col not in ['date',
                         'planetary_body_id',
                         'constellation_id',
                         'planetary_body',
                         'constellation'
                         ] and not col.endswith('_string'):
            data[col] = data[col].astype(float)
    return data


def make_forecast_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    '''Create forecast table dataframe for database insertion and returns'''
    df = data.copy()

    # Creates a new df that has all columns relevant to 'forecast' table in RDS
    # & in the correct order for insert
    forecast_dataframe = df[
        [
            'date',
            'longitude',
            'latitude',
            'planetary_body_id',
            'constellation_id',
            'right_ascension_hours',
            'right_ascension_string',
            'declination_degrees',
            'declination_string',
            'altitude_degrees',
            'altitude_string',
            'azimuth_degrees',
            'azimuth_string'
        ]
    ]

    return forecast_dataframe


def make_distance_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    '''Create distance table dataframe for database insertion and returns'''

    df = data.copy()
    df = df[
        [
            'astronomical_units',
            'planetary_body_id',
            'date'
        ]
    ]

    df['astronomical_units'] = df['astronomical_units'].astype(
        float)
    return df


def upload_to_db(forecast_df: pd.DataFrame, distance_df: pd.DataFrame, engine: Engine) -> None:
    '''Upload forecast and distance dataframes to the RDS'''
    try:
        forecast_df.to_sql(
            name='forecast',
            con=engine,
            if_exists='append',
            index=False
        )
        distance_df.to_sql(
            name='distance',
            con=engine,
            if_exists='append',
            index=False
        )
    except Exception:
        logger.info('[ERROR] Could Not Insert Into Database')


def main(data: pd.DataFrame) -> None:
    '''Bundles all functions together for one function call'''
    load_dotenv()

    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Expected a pd.DataFrame, got {type(data)}")

    if data.empty:
        raise ValueError("No Data Available")

    engine = get_db_connection()
    planetary_body_dict, constellation_dict = get_ids_from_database(engine)

    data = add_ids_to_dataframe(
        data,
        planetary_body_dict,
        constellation_dict
    )
    data = convert_types(data)

    forecast_df = make_forecast_dataframe(data)

    distance_df = make_distance_dataframe(data)

    upload_to_db(forecast_df, distance_df, engine)
    return True
