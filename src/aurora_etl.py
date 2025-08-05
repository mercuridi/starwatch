"""Mini pipeline script to extract and transform the aurora activity data, ready to be loaded on to the dashboard"""

import xmltodict
import requests
import pandas as pd


ACTIVITY_URL = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

STATUS_DESCRIPTION_URL = "http://aurorawatch-api.lancs.ac.uk/0.2/status-descriptions.xml"



def extract_status_descriptions(status_description_url: str) -> dict:
    """Returns dictionary of relevant status description data from the API response"""

    response = requests.get(status_description_url, timeout=20)
    if response.status_code != 200:
        raise RuntimeError(
            "Unable to retrieve status description data."
            "Error {response.status_code}: {response.text}")

    status_descriptions_dict = xmltodict.parse(response.content)

    return status_descriptions_dict.get("status_list").get("status")



def extract_status_description_for_colour(status_descriptions_dict: dict, colour: str) -> dict:
    """Returns a dictionary with the description and meaning for each specified colour status"""

    colour = colour.title()
    colour_order = ["Green", "Yellow", "Amber", "Red"]

    # Finds index of colour in status description
    colour_data = status_descriptions_dict[colour_order.index(colour)]

    description = colour_data.get("description").get("#text")
    meaning = colour_data.get("meaning").get("#text")

    return {colour: f"{description}: {meaning}"}


def extract_activity_data(activity_data_url: str) -> pd.DataFrame:
    """Returns dataframe of recent aurora activity data from the API response"""

    response = requests.get(activity_data_url, timeout=20)
    if response.status_code != 200:
        raise RuntimeError(
            "Unable to retrieve activity data. Error {response.status_code}: {response.text}")

    activity_dict = xmltodict.parse(response.content)
    activity_data = activity_dict.get("site_activity").get("activity")

    return pd.DataFrame(activity_data)



def find_most_recent_status_info(status_descriptions: dict, activity_data: pd.DataFrame) -> tuple[str, str, str]:
    """Returns the status colour, status description, and the date and time of the status"""

    most_recent_aurora_activity = activity_data.tail(1)

    most_recent_colour = most_recent_aurora_activity["@status_id"].values[0].title()
    most_recent_status_description = status_descriptions[most_recent_colour]

    datetime = most_recent_aurora_activity["datetime"].values[0]
    datetime_list = datetime.split("T")
    date = datetime_list[0]
    time = datetime_list[1].split("+")[0]

    return most_recent_colour, most_recent_status_description, f"{time} {date}"


# The 2 status description functions can be removed as the following dictionary can be used instead
# - this should make the dashboard more efficient as status descriptions don't rely on an API call

# Not sure if this should be left here or copied into the dashboard script
status_descriptions = {
    "Green": "No significant activity. Aurora is unlikely to be visible by "
    "eye or camera from anywhere in the UK.",
    "Yellow": "Minor geomagnetic activity. Aurora may be visible by eye from "
    "Scotland and may be visible by camera from Scotland, northern England and Northern Ireland.",
    "Amber": "Amber alert: possible aurora. Aurora is likely to be visible by eye from Scotland, "
    "northern England and Northern Ireland possibly visible from elsewhere in the UK. "
    "Photographs of aurora are likely from anywhere in the UK.",
    "Red": "Red alert: aurora likely. It is likely that aurora will be visible by eye and camera "
    "from anywhere in the UK."}

