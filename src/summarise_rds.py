"""Summary script to make long-term backup versions of daily data"""

# TODO
# Download data from RDS
# Make a summary table of the downloaded data
# Convert to JSON
# Send the JSON to the S3 bucket, named for its day
# Filepath in S3: summaries/year/month/summary-year-month-day.json
# Wrap all of the above in a lambda handler

def main():
    """Driver function"""
    pass

if __name__ == "__main__":
    main()
