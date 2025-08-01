"""Module to pull together the full ETL pipeline for the astronomy data"""

import extract_astronomy_data
import transform_astronomy_data
import load_astronomy_data
import astronomy_utils

def run_pipeline():
    """Runs the astronomy pipeline from start to finish"""
    # extract
    connection = extract_astronomy_data.get_db_connection()
    dates = extract_astronomy_data.get_date_range(connection)

    extract_astronomy_data.get_planetary_positions(
        COORDINATES,
        dates,
        str(TIME),
        astronomy_utils.make_request_headers(),
        DATA_FILEPATH
    )

    # transform
    data = transform_astronomy_data.get_json_data(FILE_PATH)

    if not isinstance(data, dict):
        raise TypeError(f"Expected to receive a dict, got {type(data)}")
    if len(data) > 0:
        transformed_data = transform_astronomy_data.filter_data(data)
        print(transformed_data)


    # load
    load_astronomy_data.main()



def handler(event, context):
    """handler function for lambda function"""
    try:
        run_pipeline()
        print(f"{event} : Lambda time remaining in MS:",
              context.get_remaining_time_in_millis())
        return {"statusCode": 200}
    except (TypeError, ValueError, IndexError) as e:
        return {"statusCode": 500, "error": str(e)}

if __name__ == "__main__":
    run_pipeline()
