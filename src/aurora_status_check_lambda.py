"""Lambda handler script to detect a red status from the aurora API"""

from src.aurora_etl import extract_activity_data, find_most_recent_status_info, is_red_colour_status



def handler(event=None, context=None):
    """Handler function to check for a red status colour from the aurora API"""

    url = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

    status_description_dict = {
        "Green": "No significant activity. Aurora is unlikely to be visible by "
        "eye or camera from anywhere in the UK.",
        "Yellow": "Minor geomagnetic activity. Aurora may be visible by eye from Scotland "
        "and may be visible by camera from Scotland, northern England and Northern Ireland.",
        "Amber": "Amber alert: possible aurora. Aurora is likely to be visible by eye from "
        "Scotland, northern England and Northern Ireland possibly visible from elsewhere in "
        "the UK. Photographs of aurora are likely from anywhere in the UK.",
        "Red": "Red alert: aurora likely. It is likely that aurora will be visible by eye "
        "and camera from anywhere in the UK."}

    activity_data = extract_activity_data(url)
    status_colour = find_most_recent_status_info(status_description_dict, activity_data)[0]

    if is_red_colour_status(status_colour):
        return {"Result": "True"}
    return {"Result": "False"}
