
import xmltodict
import requests
import pandas as pd


ACTIVITY_URL = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

STATUS_DESCRIPTION_URL = "http://aurorawatch-api.lancs.ac.uk/0.2/status-descriptions.xml"



def extract_status_descriptions(status_description_url: str) -> dict:
    """Returns dictionary of relevant status description data from the API response"""

    response = requests.get(status_description_url)
    status_descriptions_dict = xmltodict.parse(response.content)

    return status_descriptions_dict.get("status_list").get("status")



def extract_status_description_for_colour(status_descriptions_dict: dict, colour: str) -> dict:
    """Returns a dictionary with the description and meaning for each specified colour status"""

    colour = colour.title()
    colour_order = ["Green", "Yellow", "Amber", "Red"]

    colour_data = status_descriptions_dict[colour_order.index(colour)]
    description = colour_data.get("description").get("#text")
    meaning = colour_data.get("meaning").get("#text")

    return {colour: f"{description}: {meaning}"}



def extract_activity_data(activity_data_url: str) -> pd.DataFrame:
    """Returns dataframe of recent aurora activity data from the API response"""

    response = requests.get(activity_data_url)

    activity_dict = xmltodict.parse(response.content)
    activity_data = activity_dict.get("site_activity").get("activity")

    return pd.DataFrame(activity_data)
