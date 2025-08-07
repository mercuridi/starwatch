# pylint: skip-file

import pytest
import pandas as pd
from unittest.mock import MagicMock


from src.aurora_etl import extract_activity_data, find_most_recent_status_info, is_red_colour_status


def test_extract_activity_data_returns_df_correct_len(requests_mock):
    mock_xml = """<site_activity api_version="0.2.5" project_id="project: AWN">
        <updated>
            <datetime>2025-08-04T15:12:32+0000</datetime>
        </updated>
        <activity status_id="green">
            <datetime>2025-08-03T16:00:00+0000</datetime>
            <value>18.9</value>
        </activity>
        <activity status_id="green">
            <datetime>2025-08-03T17:00:00+0000</datetime>
            <value>22.5</value>
        </activity>
        </site_activity>
        """

    url = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

    requests_mock.get(url,content=mock_xml.encode("utf-8"))
    
    activity_data = extract_activity_data(url)
    
    assert requests_mock.call_count == 1
    assert len(activity_data) == 2
    assert isinstance(activity_data, pd.DataFrame)
    

def test_extract_activity_data_raises_runtime_error(requests_mock):
    mock_xml = """<site_activity api_version="0.2.5" project_id="project: AWN">
        <updated>
            <datetime>2025-08-04T15:12:32+0000</datetime>
        </updated>
        <activity status_id="green">
            <datetime>2025-08-03T16:00:00+0000</datetime>
            <value>18.9</value>
        </activity>
        <activity status_id="green">
            <datetime>2025-08-03T17:00:00+0000</datetime>
            <value>22.5</value>
        </activity>
        </site_activity>
        """

    url = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

    requests_mock.get(url, content=mock_xml.encode("utf-8"), status_code=500)

    url = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

    with pytest.raises(RuntimeError):
        extract_activity_data(url)


def test_find_most_recent_status_info_returns_tuple_correct_len():
    status_description_dict = {
        "Green": "No significant activity. Aurora is unlikely to be visible by "
        "eye or camera from anywhere in the UK."}

    example_activity_data = pd.DataFrame({"@status_id": ["green"],
                                          "datetime": ["2025-08-04T18:00:00+0000"],
                        "value": ["17.6"]})

    status_info = find_most_recent_status_info(status_description_dict, example_activity_data)

    assert isinstance(status_info, tuple)
    assert len(status_info) == 3



def test_find_most_recent_status_info_correct_data():
    status_description_dict = {
        "Green": "No significant activity. Aurora is unlikely to be visible by "
        "eye or camera from anywhere in the UK."}

    example_activity_data = pd.DataFrame({"@status_id": ["green"],
                                          "datetime": ["2025-08-04T18:00:00+0000"],
                        "value": ["17.6"]})

    status_info = find_most_recent_status_info(status_description_dict, example_activity_data)

    assert status_info[0] == "Green"
    assert status_info[1] == "No significant activity. Aurora is unlikely to be visible by eye or camera from anywhere in the UK."
    assert status_info[2] == "18:00 PM, Mon 04 Aug"



def test_find_most_recent_status_info_handles_error():
    status_description_dict = {
        "Green": "No significant activity. Aurora is unlikely to be visible by "
        "eye or camera from anywhere in the UK."}
    mock_activity_data = MagicMock()
    mock_activity_data.tail.side_effect = RuntimeError()

    with pytest.raises(RuntimeError):
        find_most_recent_status_info(status_description_dict, mock_activity_data)


def test_is_red_colour_status_true():
    assert is_red_colour_status("Red") == True


def test_is_red_colour_status_false():
    assert is_red_colour_status("Green") == False


def test_is_red_colour_status_wrong_type():
    assert is_red_colour_status(0) == False
