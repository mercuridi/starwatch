# pylint: skip-file


from src.aurora_etl import extract_activity_data, find_most_recent_status_info


def test_extract_activity_data(requests_mock):
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
    