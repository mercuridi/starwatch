# pylint: skip-file
import pandas as pd
from unittest.mock import MagicMock, patch

from src.load_astronomy_data import (
    get_db_connection,
    get_transformed_data,
    get_ids_from_database,
    add_ids_to_dataframe,
    convert_types,
    make_forecast_dataframe,
    make_distance_dataframe,
    upload_to_db,
    main
)


# Test for transformed data retrieval
@patch("src.load_astronomy_data.get_json_data")
@patch("src.load_astronomy_data.filter_data")
def test_get_transformed_data_returns_dataframe(mock_filter_data, mock_get_json_data):
    mock_df = pd.DataFrame({"planetary_body": ["Mars"]})
    mock_get_json_data.return_value = {}
    mock_filter_data.return_value = mock_df

    result = get_transformed_data()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


# Test for correctly getting ids for mapping
def test_get_ids_from_database_returns_dicts():
    mock_engine = MagicMock()
    mock_conn = mock_engine.connect.return_value.__enter__.return_value

    mock_result_1 = MagicMock()
    mock_result_1.fetchall.return_value = [(1, "Mars"), (2, "Venus")]

    mock_result_2 = MagicMock()
    mock_result_2.fetchall.return_value = [(10, "Orion"), (11, "Scorpius")]

    mock_conn.execute.side_effect = [mock_result_1, mock_result_2]

    planetary_body_dict_test, constellation_dict_test = get_ids_from_database(
        mock_engine)

    assert planetary_body_dict_test == {"Mars": 1, "Venus": 2}
    assert constellation_dict_test == {"Orion": 10, "Scorpius": 11}


# Test for correct mapping of ids to values
def test_add_ids_to_dataframe_maps_ids_correctly():
    data = pd.DataFrame({
        "planetary_body": ["Mars", "Venus"],
        "constellation": ["Orion", "Scorpius"]
    })
    planetary_body_map = {"Mars": 1, "Venus": 2}
    constellation_map = {"Orion": 10, "Scorpius": 11}

    result = add_ids_to_dataframe(data, planetary_body_map, constellation_map)
    assert result["planetary_body_id"].tolist() == [1, 2]
    assert result["constellation_id"].tolist() == [10, 11]


# Test for converting columns to correct data type
def test_convert_types_converts_numerical_columns():
    data = pd.DataFrame({
        "astronomical_units": ["1.2", "2.5"],
        "planetary_body_string": ["Mars", "Venus"],
        "date": ["2025-01-01", "2025-01-02"],
        "planetary_body_id": [1, 3]
    })

    result = convert_types(data)

    assert result["astronomical_units"].dtype == float
    assert result["date"].dtype == object
    assert result["planetary_body_string"].dtype == "string"
    assert result["planetary_body_id"].dtype == int


# Tests for making the forecast dataframe
def test_make_forecast_dataframe_columns():
    data = pd.DataFrame({
        "date": ["2025-01-01"],
        "longitude": [1.0],
        "latitude": [1.0],
        "planetary_body_id": [1],
        "constellation_id": [2],
        "right_ascension_hours": [10],
        "right_ascension_string": ["09h 01m 12s"],
        "declination_degrees": [20],
        "declination_string": ["-29° 37' 12"],
        "altitude_degrees": [5],
        "altitude_string": ["46° 35' 24"],
        "azimuth_degrees": [30],
        "azimuth_string": ["324° 43' 12"]
    })

    result = make_forecast_dataframe(data)
    assert list(result.columns) == [
        'date', 'longitude', 'latitude', 'planetary_body_id', 'constellation_id',
        'right_ascension_hours', 'right_ascension_string',
        'declination_degrees', 'declination_string',
        'altitude_degrees', 'altitude_string',
        'azimuth_degrees', 'azimuth_string'
    ]


# Tests for making the distance dataframe
def test_make_distance_dataframe_valid():
    df = pd.DataFrame({
        'astronomical_units': ["1.01432", "0.00257"],
        'planetary_body_id': [1, 2],
        'date': ["2025-01-01", "2025-01-02"]
    })
    result = make_distance_dataframe(df)
    assert list(result.columns) == [
        'astronomical_units', 'planetary_body_id', 'date']
    assert result['astronomical_units'].dtype == float


# Tests for the inserting of both forecast and distance dataframes into the RDS
@patch("pandas.DataFrame.to_sql")
def test_upload_to_db_calls_to_sql(mock_to_sql):
    df_forecast_test = pd.DataFrame({
        "date": ["2025-01-01"],
        "longitude": [1.0],
        "latitude": [1.0],
        "planetary_body_id": [1],
        "constellation_id": [2],
        "right_ascension_hours": [10],
        "right_ascension_string": ["09h 01m 12s"],
        "declination_degrees": [20],
        "declination_string": ["-29° 37' 12"],
        "altitude_degrees": [5],
        "altitude_string": ["46° 35' 24"],
        "azimuth_degrees": [30],
        "azimuth_string": ["324° 43' 12"]
    })

    df_distance_test = pd.DataFrame({
        'astronomical_units': [1.0],
        'planetary_body_id': [1],
        'date': ['2025-01-01']
    })
    engine = MagicMock()

    upload_to_db(df_forecast_test, df_distance_test, engine)
    assert mock_to_sql.call_count == 2
