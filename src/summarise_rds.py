"""Summary script to make long-term backup versions of daily data"""
import os

import dotenv
import psycopg2
import pandas as pd

# TODO
# Download data from RDS (DONE)
# Make a summary table of the downloaded data
# Convert to JSON
# Send the JSON to the S3 bucket, named for its day
# Filepath in S3: summaries/year/month/summary-year-month-day.json
# Wrap all of the above in a lambda handler

def main():
    """Driver function"""
    conn_string = f"host='{os.environ["db_host"]}' dbname='{os.environ["db_name"]}' user='{os.environ["db_username"]}' password='{os.environ["db_password"]}'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute("select * from forecast;")
    val = pd.DataFrame(cur.fetchall())
    print(val)
    cur.close()
    conn.close()

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
