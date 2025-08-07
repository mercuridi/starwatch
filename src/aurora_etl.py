"""Mini pipeline script to extract and transform the aurora activity data, 
ready to be loaded on to the dashboard"""

from datetime import datetime

import xmltodict
import requests
import pandas as pd

ACTIVITY_URL = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"


def extract_activity_data(activity_data_url: str) -> pd.DataFrame:
    """Returns dataframe of recent aurora activity data from the API response"""

    response = requests.get(activity_data_url, timeout=20)
    if response.status_code != 200:
        raise RuntimeError("Unable to retrieve activity data. "
                           f"Error {response.status_code}: {response.text}")

    activity_dict = xmltodict.parse(response.content)
    activity_data = activity_dict.get("site_activity").get("activity")

    return pd.DataFrame(activity_data)


def find_most_recent_status_info(status_descriptions: dict,
                                 activity_data: pd.DataFrame) -> tuple[str, str, str]:
    """Returns the status colour, status description, and the date and time of the status"""

    most_recent_aurora_activity = activity_data.tail(1)

    most_recent_colour = most_recent_aurora_activity["@status_id"].values[0].title(
    )
    most_recent_status_description = status_descriptions[most_recent_colour]

    # Convert datetime data into more readable format
    date_time = most_recent_aurora_activity["datetime"].values[0]
    datetime_obj = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z")
    datetime_str = datetime_obj.strftime("%H:%M %p, %a %d %b")

    return most_recent_colour, most_recent_status_description, datetime_str


def is_red_colour_status(status_colour: str) -> bool:
    """Returns true if aurora status colour is red"""
    if status_colour == "Red":
        return True
    return False
