"""Summary script to make long-term backup versions of daily data"""
import os
import datetime

import dotenv
import psycopg2
import pandas as pd
import boto3
from botocore.exceptions import ClientError

TEMP_FILE_PATH = "../data/temp_data.json"

# TODO
# Download data from RDS (DONE)
# Make a summary table of the downloaded data
# Convert to JSON
# Send the JSON to the S3 bucket, named for its day
# Filepath in S3: summaries/year/month/summary-year-month-day.json
# Wrap all of the above in a lambda handler

def main():
    """Driver function"""
    conn_string = f"""
    host='{os.environ["db_host"]}'
    dbname='{os.environ["db_name"]}'
    user='{os.environ["db_username"]}'
    password='{os.environ["db_password"]}'
    """
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute("select * from constellation;")
    df = pd.DataFrame(cur.fetchall())
    cur.close()
    conn.close()
    df.to_json(TEMP_FILE_PATH, indent=2)

    today_date = datetime.date.today()
    s3_path = f"{today_date.year}/{today_date.month}/summary-{today_date.year}-{today_date.month}-{today_date.day}.json"

    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(TEMP_FILE_PATH, "c18-starwatch-s3", s3_path)
    except ClientError as e:
        print(e)

    os.remove(TEMP_FILE_PATH)



if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
